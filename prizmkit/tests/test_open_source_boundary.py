import re
import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
RETRO_SKILL_DIR = SKILL_DIR.parent / "prizmkit-retrospective"
EXECUTION_LAYER_PATTERNS = (
    r"l" + r"4-headless",
    r"prizmkit-l" + r"4",
    r"L" + r"1\s+(?:toolkit|workflow|state|metadata|stage|runtime)",
    r"(?:composite|atomic)\s+L" + r"1",
    r"L" + r"2\s+(?:pipeline|batch|orchestration|planner|launcher)",
)


class OpenSourceBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill_files = [
            path
            for path in SKILL_DIR.parent.rglob("*")
            if path.is_file()
            and path.suffix in {".md", ".json", ".py"}
            and "tests" not in path.parts
            and "__pycache__" not in path.parts
        ]
        cls.retrospective = (RETRO_SKILL_DIR / "SKILL.md").read_text()
        cls.structural_sync = (
            RETRO_SKILL_DIR / "references" / "structural-sync-steps.md"
        ).read_text()
        cls.knowledge_injection = (
            RETRO_SKILL_DIR / "references" / "knowledge-injection-steps.md"
        ).read_text()

    def test_execution_architecture_terms_are_not_exposed(self):
        # The numbered names in prizm-docs content describe documentation levels,
        # not internal execution architecture, so this contract targets only
        # execution-specific phrases.
        for path in self.skill_files:
            content = path.read_text()
            for pattern in EXECUTION_LAYER_PATTERNS:
                self.assertIsNone(
                    re.search(pattern, content, re.IGNORECASE),
                    f"{path}: {pattern}",
                )

    def test_retrospective_excludes_prizmkit_tree_from_change_input(self):
        for phrase in [
            "exact caller-supplied non-`.prizmkit/` `change_paths`",
            "Reject paths outside the checkout, paths under `.prizmkit/`",
        ]:
            self.assertIn(phrase, self.retrospective)
        self.assertIn(
            "reject paths outside the checkout or under `.prizmkit/`",
            self.structural_sync,
        )
        for phrase in [
            "never broaden the diff",
            "Existing affected Prizm docs may be read only as update targets",
        ]:
            self.assertIn(phrase, self.knowledge_injection)


if __name__ == "__main__":
    unittest.main()
