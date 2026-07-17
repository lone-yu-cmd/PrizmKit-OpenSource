#!/usr/bin/env python3
"""Validate the independent PrizmKit L1 skill release package."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "prizmkit",
    "prizmkit-workflow",
    "prizmkit-init",
    "prizmkit-plan",
    "prizmkit-implement",
    "prizmkit-code-review",
    "prizmkit-test",
    "prizmkit-retrospective",
    "prizmkit-committer",
    "prizmkit-prizm-docs",
    "prizmkit-deploy",
}
LIFECYCLE = [
    "prizmkit-plan",
    "prizmkit-implement",
    "prizmkit-code-review",
    "prizmkit-test",
    "prizmkit-retrospective",
    "prizmkit-committer",
]
FORBIDDEN_SKILL_DEPENDENCIES = (
    "app-planner",
    "feature-planner",
    "bug-planner",
    "refactor-planner",
    "feature-pipeline-launcher",
    "bugfix-pipeline-launcher",
    "refactor-pipeline-launcher",
    "feature-workflow",
    "dev-pipeline/",
)
SKILL_DIR_REFERENCE = re.compile(r"\$\{SKILL_DIR\}/([^\s`)>\]}]+)")
FRONTMATTER = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)


class Validation:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.checked: list[str] = []

    def check(self, condition: bool, message: str) -> None:
        if condition:
            self.checked.append(message)
        else:
            self.errors.append(message)

    def file(self, relative: str) -> Path:
        path = ROOT / relative
        self.check(path.is_file(), f"missing file: {relative}")
        return path


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(path: Path, validation: Validation) -> dict[str, str]:
    match = FRONTMATTER.match(read(path))
    validation.check(match is not None, f"valid frontmatter: {path.relative_to(ROOT)}")
    if not match:
        return {}

    values: dict[str, str] = {}
    for line in match.group("body").splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip().strip('"')
    validation.check("name" in values, f"frontmatter name: {path.relative_to(ROOT)}")
    validation.check(
        "description" in values,
        f"frontmatter description: {path.relative_to(ROOT)}",
    )
    return values


def owning_skill(path: Path) -> Path | None:
    for parent in path.parents:
        if parent.parent == ROOT:
            return parent
    return None


def validate_skill_inventory(validation: Validation) -> list[Path]:
    skill_dirs = sorted(path for path in ROOT.iterdir() if path.is_dir() and (path / "SKILL.md").is_file())
    names = {path.name for path in skill_dirs}
    validation.check(names == EXPECTED_SKILLS, f"skill inventory: {sorted(EXPECTED_SKILLS)}")

    skill_files: list[Path] = []
    for skill_dir in skill_dirs:
        skill_file = skill_dir / "SKILL.md"
        skill_files.append(skill_file)
        frontmatter = parse_frontmatter(skill_file, validation)
        validation.check(
            frontmatter.get("name") == skill_dir.name,
            f"frontmatter name matches directory: {skill_dir.name}",
        )
    return skill_files


def validate_local_references(validation: Validation) -> None:
    references = 0
    for document in sorted(ROOT.rglob("*.md")):
        if "__pycache__" in document.parts:
            continue
        owner = owning_skill(document)
        if owner is None:
            continue
        text = read(document)
        for match in SKILL_DIR_REFERENCE.finditer(text):
            references += 1
            relative = match.group(1).rstrip(".,;:")
            target = (owner / relative).resolve()
            try:
                target.relative_to(owner.resolve())
            except ValueError:
                validation.errors.append(
                    f"SKILL_DIR reference escapes owning skill: {document.relative_to(ROOT)} -> {relative}"
                )
                continue
            validation.check(
                target.exists(),
                f"local reference exists: {document.relative_to(ROOT)} -> {relative}",
            )
    validation.check(references > 0, "local SKILL_DIR references discovered")


def validate_lifecycle(validation: Validation, skill_files: list[Path]) -> None:
    lifecycle_text = "\n".join(read(ROOT / name / "SKILL.md") for name in LIFECYCLE)
    for skill in LIFECYCLE:
        validation.check(skill in lifecycle_text, f"lifecycle skill named: {skill}")

    for document in [ROOT / "README.md", ROOT / "README.zh-CN.md", ROOT / "prizmkit" / "SKILL.md"]:
        text = read(document)
        positions = [text.find(skill) for skill in LIFECYCLE]
        validation.check(
            all(position >= 0 for position in positions) and positions == sorted(positions),
            f"lifecycle order: {document.relative_to(ROOT)}",
        )

    for skill_file in skill_files:
        text = read(skill_file)
        for forbidden in FORBIDDEN_SKILL_DEPENDENCIES:
            validation.check(
                not re.search(rf"(?<![A-Za-z0-9_-]){re.escape(forbidden)}(?![A-Za-z0-9_-])", text),
                f"no hidden L2 dependency in {skill_file.relative_to(ROOT)}: {forbidden}",
            )


def validate_repository_docs(validation: Validation) -> None:
    required_files = [
        "README.md",
        "README.zh-CN.md",
        "WORKFLOW-STATE.md",
        "LICENSE",
        "CONTRIBUTING.md",
        "SECURITY.md",
        "CODE_OF_CONDUCT.md",
        "CHANGELOG.md",
        ".gitignore",
    ]
    for relative in required_files:
        validation.file(relative)

    english = read(ROOT / "README.md")
    chinese = read(ROOT / "README.zh-CN.md")
    for phrase in (
        "plan → implement → code-review → test → retrospective → committer",
        "npx skills add",
        "prizmkit-init",
        "prizmkit-prizm-docs",
        "prizmkit-deploy",
        "prizmkit-workflow",
        "app-planner",
        "WORKFLOW-STATE.md",
    ):
        validation.check(phrase in english, f"English README includes: {phrase}")
    for phrase in (
        "plan → implement → code-review → test → retrospective → committer",
        "npx skills add",
        "prizmkit-init",
        "prizmkit-prizm-docs",
        "prizmkit-deploy",
        "prizmkit-workflow",
        "WORKFLOW-STATE.md",
    ):
        validation.check(phrase in chinese, f"Chinese README includes: {phrase}")


def validate_generated_files(validation: Validation) -> None:
    generated = [
        path
        for path in ROOT.rglob("*")
        if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}
    ]
    validation.check(not generated, "no Python cache or bytecode files")
    for path in generated:
        validation.errors.append(f"generated file must not ship: {path.relative_to(ROOT)}")


def main() -> int:
    validation = Validation()
    skill_files = validate_skill_inventory(validation)
    validate_local_references(validation)
    validate_lifecycle(validation, skill_files)
    validate_repository_docs(validation)
    validate_generated_files(validation)

    if validation.errors:
        print(f"RELEASE_FAIL ({len(validation.errors)} errors)")
        for error in validation.errors:
            print(f"- {error}")
        return 1

    print(f"RELEASE_PASS ({len(validation.checked)} checks)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
