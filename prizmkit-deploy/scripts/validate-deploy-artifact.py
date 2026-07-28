#!/usr/bin/env python3
"""Validate non-sensitive semantic invariants for PrizmKit Deploy artifacts.

This companion validator is intentionally read-only and standard-library-only.
JSON Schema validation remains mandatory; this script enforces cross-field and
host-neutral path rules that are awkward to express or easy to regress in a
schema alone. Diagnostics contain stable codes and JSON paths, never values.
"""

from __future__ import annotations

import argparse
import json
import re
import stat
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

MAX_INPUT_BYTES = 1024 * 1024
MAX_ERRORS = 50
VERIFICATION_LAYERS = {
    "command_or_platform",
    "runtime_or_release",
    "configured_health",
    "external_url",
    "startup_logs",
}
FORBIDDEN_FIELDS = {
    "value",
    "secret_value",
    "password",
    "token",
    "private_key",
    "connection_string",
    "raw_output",
    "raw_logs",
}
_SAFE_KEY = re.compile(r"^[A-Za-z_][A-Za-z0-9_]{0,63}$")
_DRIVE_PREFIX = re.compile(r"^[A-Za-z]:")


class DuplicateKeyError(ValueError):
    """Raised for a duplicate object key without retaining its key or value."""


@dataclass(frozen=True, order=True)
class ValidationError:
    code: str
    path: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "path": self.path}


class ErrorCollector:
    """Collect a bounded deterministic set of non-sensitive diagnostics."""

    def __init__(self) -> None:
        self._errors: set[ValidationError] = set()

    def add(self, code: str, path: str) -> None:
        if len(self._errors) >= MAX_ERRORS:
            return
        self._errors.add(ValidationError(code=code, path=path))

    def result(self) -> list[dict[str, str]]:
        return [error.as_dict() for error in sorted(self._errors)]


def _strict_object(pairs: Sequence[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise DuplicateKeyError("duplicate JSON key")
        result[key] = value
    return result


def _load_json(path: Path) -> tuple[Any | None, list[dict[str, str]]]:
    try:
        metadata = path.lstat()
    except OSError:
        return None, [{"code": "INPUT_UNREADABLE", "path": "$"}]
    if path.is_symlink() or not stat.S_ISREG(metadata.st_mode):
        return None, [{"code": "INPUT_NOT_REGULAR_FILE", "path": "$"}]
    if metadata.st_size > MAX_INPUT_BYTES:
        return None, [{"code": "INPUT_TOO_LARGE", "path": "$"}]
    try:
        content = path.read_text(encoding="utf-8")
        return json.loads(content, object_pairs_hook=_strict_object), []
    except DuplicateKeyError:
        return None, [{"code": "DUPLICATE_KEY", "path": "$"}]
    except (OSError, UnicodeError, json.JSONDecodeError, RecursionError):
        return None, [{"code": "INVALID_JSON", "path": "$"}]


def _is_project_relative_path(value: Any, *, allow_root: bool = False) -> bool:
    if not isinstance(value, str) or not value or len(value) > 512:
        return False
    if value == ".":
        return allow_root
    if value.startswith("/") or _DRIVE_PREFIX.match(value) or "\\" in value:
        return False
    if any(unicodedata.category(character) in {"Cc", "Cs"} for character in value):
        return False
    parts = value.split("/")
    return all(part not in {"", ".", ".."} for part in parts)


def _is_legacy_deploy_path(value: Any) -> bool:
    return _is_project_relative_path(value) and str(value).startswith(".prizmkit/deploy/")


def _iter_list(value: Any) -> Iterable[tuple[int, Any]]:
    if not isinstance(value, list):
        return ()
    return enumerate(value)


def _check_path_list(
    value: Any,
    path: str,
    errors: ErrorCollector,
    *,
    legacy: bool = False,
) -> None:
    predicate = _is_legacy_deploy_path if legacy else _is_project_relative_path
    for index, item in _iter_list(value):
        if not predicate(item):
            errors.add("UNSAFE_MANAGED_PATH", f"{path}[{index}]")


def _check_forbidden_fields(value: Any, path: str, errors: ErrorCollector) -> None:
    pending: list[tuple[Any, str]] = [(value, path)]
    while pending:
        current, current_path = pending.pop()
        if isinstance(current, Mapping):
            for key, child in current.items():
                child_path = (
                    f"{current_path}.{key}"
                    if _SAFE_KEY.fullmatch(str(key))
                    else f"{current_path}.[unknown]"
                )
                if str(key).lower() in FORBIDDEN_FIELDS:
                    errors.add("FORBIDDEN_SENSITIVE_FIELD", child_path)
                pending.append((child, child_path))
        elif isinstance(current, list):
            pending.extend(
                (child, f"{current_path}[{index}]")
                for index, child in enumerate(current)
            )


def _check_unique_names(
    value: Any,
    path: str,
    field: str,
    code: str,
    errors: ErrorCollector,
) -> set[str]:
    seen: set[str] = set()
    for index, item in _iter_list(value):
        if not isinstance(item, Mapping):
            continue
        identity = item.get(field)
        if not isinstance(identity, str):
            continue
        if identity in seen:
            errors.add(code, f"{path}[{index}].{field}")
        seen.add(identity)
    return seen


def _check_profile_reference(
    value: Any,
    path: str,
    profiles: set[str],
    errors: ErrorCollector,
) -> None:
    if value is not None and isinstance(value, str) and value not in profiles:
        errors.add("DANGLING_PROFILE_REFERENCE", path)


def _check_terminal_result(value: Any, path: str, errors: ErrorCollector) -> None:
    if not isinstance(value, Mapping):
        return
    verification = value.get("verification")
    if not isinstance(verification, list):
        errors.add("VERIFICATION_LAYER_SET", f"{path}.verification")
        return

    layers: list[str] = []
    for item in verification:
        if isinstance(item, Mapping) and isinstance(item.get("layer"), str):
            layers.append(item["layer"])
    if len(verification) != len(VERIFICATION_LAYERS) or set(layers) != VERIFICATION_LAYERS:
        errors.add("VERIFICATION_LAYER_SET", f"{path}.verification")
    if len(layers) != len(set(layers)):
        errors.add("DUPLICATE_VERIFICATION_LAYER", f"{path}.verification")

    if value.get("status") == "SUCCEEDED":
        for index, item in _iter_list(verification):
            if (
                isinstance(item, Mapping)
                and item.get("required") is True
                and item.get("status") != "PASSED"
            ):
                errors.add(
                    "SUCCEEDED_REQUIRED_LAYER_NOT_PASSED",
                    f"{path}.verification[{index}]",
                )


def _validate_record(data: Any, errors: ErrorCollector) -> None:
    if not isinstance(data, Mapping):
        errors.add("ROOT_NOT_OBJECT", "$")
        return

    project = data.get("project")
    if isinstance(project, Mapping):
        _check_path_list(
            project.get("native_config_files"),
            "$.project.native_config_files",
            errors,
        )

    profiles_value = data.get("profiles")
    profiles = _check_unique_names(
        profiles_value,
        "$.profiles",
        "id",
        "DUPLICATE_PROFILE_ID",
        errors,
    )
    for index, profile in _iter_list(profiles_value):
        if isinstance(profile, Mapping):
            _check_path_list(
                profile.get("native_config_files"),
                f"$.profiles[{index}].native_config_files",
                errors,
            )

    _check_unique_names(
        data.get("secret_references"),
        "$.secret_references",
        "name",
        "DUPLICATE_SECRET_REFERENCE",
        errors,
    )

    current = data.get("current")
    if isinstance(current, Mapping):
        _check_profile_reference(
            current.get("profile_id"),
            "$.current.profile_id",
            profiles,
            errors,
        )

    latest = data.get("latest_result")
    if isinstance(latest, Mapping):
        _check_profile_reference(
            latest.get("profile_id"),
            "$.latest_result.profile_id",
            profiles,
            errors,
        )
        _check_terminal_result(latest, "$.latest_result", errors)

    for index, history in _iter_list(data.get("history")):
        if isinstance(history, Mapping):
            _check_profile_reference(
                history.get("profile_id"),
                f"$.history[{index}].profile_id",
                profiles,
                errors,
            )

    recovery = data.get("recovery")
    if isinstance(recovery, Mapping):
        _check_profile_reference(
            recovery.get("profile_id"),
            "$.recovery.profile_id",
            profiles,
            errors,
        )

    legacy = data.get("legacy_migration")
    if isinstance(legacy, Mapping):
        sources = legacy.get("sources")
        for index, source in _iter_list(sources):
            if isinstance(source, Mapping) and not _is_legacy_deploy_path(source.get("path")):
                errors.add("UNSAFE_MANAGED_PATH", f"$.legacy_migration.sources[{index}].path")
        _check_path_list(
            legacy.get("preserved_paths"),
            "$.legacy_migration.preserved_paths",
            errors,
            legacy=True,
        )


def _validate_declaration(data: Any, errors: ErrorCollector) -> None:
    if not isinstance(data, Mapping):
        errors.add("ROOT_NOT_OBJECT", "$")
        return

    _check_path_list(data.get("native_config_files"), "$.native_config_files", errors)
    _check_unique_names(
        data.get("profile_hints"),
        "$.profile_hints",
        "id",
        "DUPLICATE_PROFILE_ID",
        errors,
    )
    _check_unique_names(
        data.get("secret_references"),
        "$.secret_references",
        "name",
        "DUPLICATE_SECRET_REFERENCE",
        errors,
    )

    for index, command in _iter_list(data.get("commands")):
        if (
            isinstance(command, Mapping)
            and not _is_project_relative_path(command.get("working_directory"), allow_root=True)
        ):
            errors.add("UNSAFE_MANAGED_PATH", f"$.commands[{index}].working_directory")

    for index, hint in _iter_list(data.get("capability_hints")):
        if isinstance(hint, Mapping):
            _check_path_list(
                hint.get("evidence_files"),
                f"$.capability_hints[{index}].evidence_files",
                errors,
            )


def validate(kind: str, data: Any) -> list[dict[str, str]]:
    errors = ErrorCollector()
    _check_forbidden_fields(data, "$", errors)
    if kind == "record":
        _validate_record(data, errors)
    else:
        _validate_declaration(data, errors)
    return errors.result()


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Validate semantic invariants for one PrizmKit Deploy artifact."
    )
    parser.add_argument("--kind", choices=("record", "declaration"), required=True)
    parser.add_argument("path", type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    data, load_errors = _load_json(args.path)
    errors = load_errors or validate(args.kind, data)
    output = {"valid": not errors, "errors": errors}
    print(json.dumps(output, ensure_ascii=False, separators=(",", ":")))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
