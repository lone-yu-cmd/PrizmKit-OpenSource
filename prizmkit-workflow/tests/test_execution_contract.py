import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]


class WorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_DIR / "SKILL.md").read_text()
        cls.state = (SKILL_DIR / "references" / "workflow-state-protocol.md").read_text()

    def test_coordinates_all_six_stages_in_order(self):
        stages = [
            "prizmkit-plan",
            "prizmkit-implement",
            "prizmkit-code-review",
            "prizmkit-test",
            "prizmkit-retrospective",
            "prizmkit-committer",
        ]
        positions = [self.skill.index(stage) for stage in stages]
        self.assertEqual(positions, sorted(positions))
        for stage in stages:
            self.assertIn(stage, self.skill)

    def test_preserves_artifact_identity_and_workflow_state(self):
        required = [
            "same `artifact_dir`",
            ".prizmkit/state/workflows/<requirement-slug>.json",
            "workflow-state-protocol.md",
            "Never select a different most-recent plan",
        ]
        for phrase in required:
            self.assertIn(phrase, self.skill)

    def test_requires_truthful_stage_success(self):
        required = [
            "Advance Only on Truthful Success",
            "PLAN_READY",
            "IMPLEMENTED",
            "REVIEW_PASS",
            "TEST_PASS",
            "DOCS_UPDATED",
            "NO_DOC_CHANGE",
            "COMMITTED",
        ]
        for phrase in required:
            self.assertIn(phrase, self.skill)

    def test_routes_failures_by_repair_scope(self):
        required = [
            "TEST_FAIL affecting only tests",
            "TEST_FAIL affecting production code",
            "TEST_BLOCKED",
            "do not make speculative production edits",
            "at most three automatic repair rounds",
        ]
        for phrase in required:
            self.assertIn(phrase, self.skill)

    def test_commit_requires_confirmation(self):
        required = [
            "must not silently create a Git commit",
            "wait for explicit user confirmation",
            "Remote push is never part",
        ]
        for phrase in required:
            self.assertIn(phrase, self.skill)

    def test_supports_manual_handoff_and_resume(self):
        required = [
            "semantic skill-to-skill invocation",
            "one exact recovery instruction",
            "Continue from the first incomplete stage",
            "same `artifact_dir`",
        ]
        for phrase in required:
            self.assertIn(phrase, self.skill)

    def test_state_reference_describes_repair_routing(self):
        for phrase in [
            "TEST_FAIL with repair_scope=test-infrastructure",
            "TEST_FAIL with repair_scope=production",
            "TEST_BLOCKED",
            "at most three automatic repair rounds",
        ]:
            self.assertIn(phrase, self.state)


if __name__ == "__main__":
    unittest.main()
