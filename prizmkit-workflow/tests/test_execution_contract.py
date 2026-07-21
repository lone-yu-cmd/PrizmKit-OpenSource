import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ATOMIC_SKILLS = {
    "plan": SKILL_DIR / "../prizmkit-plan/SKILL.md",
    "implement": SKILL_DIR / "../prizmkit-implement/SKILL.md",
    "code-review": SKILL_DIR / "../prizmkit-code-review/SKILL.md",
    "test": SKILL_DIR / "../prizmkit-test/SKILL.md",
    "retrospective": SKILL_DIR / "../prizmkit-retrospective/SKILL.md",
    "committer": SKILL_DIR / "../prizmkit-committer/SKILL.md",
}
STATE_REFERENCES = [
    SKILL_DIR / "references/workflow-state-protocol.md",
    *(
        path.parent / "references" / "workflow-state-protocol.md"
        for name, path in ATOMIC_SKILLS.items()
        if name != "test"
    ),
]


class WorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_DIR / "SKILL.md").read_text()
        cls.state = (SKILL_DIR / "references" / "workflow-state-protocol.md").read_text()
        cls.atomic = {name: path.resolve().read_text() for name, path in ATOMIC_SKILLS.items()}
        cls.subagent = (SKILL_DIR / "../prizmkit-implement/references/implementation-subagent-procedure.md").resolve().read_text()

    def test_coordinates_exactly_six_mandatory_stages_in_order(self):
        stages = [
            "prizmkit-plan", "prizmkit-implement", "prizmkit-code-review",
            "prizmkit-test", "prizmkit-retrospective", "prizmkit-committer",
        ]
        positions = [self.skill.index(stage) for stage in stages]
        self.assertEqual(positions, sorted(positions))
        self.assertIn("The six stages are mandatory", self.skill)

    def test_preserves_artifact_identity_and_separate_external_state(self):
        for phrase in [
            "same `artifact_dir`",
            ".prizmkit/state/workflows/<requirement-slug>.json",
            ".prizmkit/specs/<requirement-slug>/",
            ".prizmkit/bugfix/<bug-id>/",
            ".prizmkit/refactor/<refactor-id>/",
            "external host execution checkpoint",
            "Never select a different most-recent plan",
        ]:
            self.assertIn(phrase, self.skill)
        self.assertIn("External host checkpoint", self.state)

    def test_state_indexes_skill_owned_test_artifacts(self):
        for field in [
            '"artifact_dir"', '"stage"', '"status"', '"stage_result"',
            '"completed_stages"', '"repair_scope"', '"repair_round"',
            '"next_stage"', '"resume_from"',
        ]:
            self.assertIn(field, self.state)
        for phrase in [
            "The state file is an index",
            "`{artifact_dir}/test-report.md`",
            "`{artifact_dir}/test-result.json`",
            "Git history and confirmed or authorized commit identity",
        ]:
            self.assertIn(phrase, self.state)

    def test_maps_all_three_l1_test_results(self):
        for phrase in [
            "test-result TEST_PASS",
            "status=completed,  stage_result=TEST_PASS",
            "test-result TEST_NEEDS_FIXES",
            "status=failed,     stage_result=TEST_NEEDS_FIXES",
            "test-result TEST_BLOCKED",
            "status=failed,     stage_result=TEST_BLOCKED",
        ]:
            self.assertIn(phrase, self.state)
        self.assertNotIn("TEST_FAIL", self.state)
        self.assertNotIn("TEST_FAIL", self.skill)

    def test_test_non_pass_stops_without_l1_runtime_knowledge(self):
        for phrase in [
            "TEST_NEEDS_FIXES",
            "TEST_BLOCKED",
            "caller owns any later review/retest decision",
            "must never treat either result as an AI CLI crash",
        ]:
            self.assertIn(phrase, self.skill)
        for phrase in [
            "A test result is not an AI CLI session classification",
            "caller or external host owns recovery policy",
            "internal to one test invocation",
        ]:
            self.assertIn(phrase, self.state)

    def test_test_skill_owns_internal_review_and_repair_budgets(self):
        test = self.atomic["test"]
        self.assertIn("Use at most ten completed rounds", test)
        self.assertIn("at most five responses", test)
        self.assertIn("Use at most three execution-failure repair rounds", test)
        self.assertIn("must not", test)
        self.assertIn("update a workflow checkpoint or pipeline runtime state", test)
        self.assertNotIn("workflow-state-protocol.md", test)

    def test_atomic_skills_do_not_recursively_invoke_handoffs(self):
        expected = {
            "plan": "must not invoke `prizmkit-implement` itself",
            "implement": "must not invoke code review or test itself",
            "code-review": "must not invoke `prizmkit-test` or `prizmkit-implement` itself",
            "retrospective": "must not invoke `prizmkit-committer` itself",
            "committer": "must not invoke deployment or any hidden seventh stage",
        }
        for name, phrase in expected.items():
            self.assertIn(phrase, self.atomic[name])
        self.assertIn("After writing its result, this skill returns control to its caller", self.atomic["test"])

    def test_retrospective_and_commit_still_require_test_pass(self):
        self.assertIn("`TEST_NEEDS_FIXES` or `TEST_BLOCKED` remains unresolved", self.atomic["retrospective"])
        self.assertIn("tests have `TEST_NEEDS_FIXES`/`TEST_BLOCKED`", self.atomic["committer"])
        self.assertIn("consistent `test-report.md`/`test-result.json` pair", self.atomic["committer"])

    def test_commit_modes_remain_separate(self):
        for phrase in [
            '"mode": "<host-defined-headless-mode>"',
            "local_commit_authorized=true",
            "Remote publication is outside this atomic commit stage",
        ]:
            self.assertIn(phrase, self.atomic["committer"])
        self.assertIn("wait for explicit user confirmation from the current user", self.skill)

    def test_implementation_subagent_checkout_boundary_is_unchanged(self):
        for phrase in [
            "same active checkout", "Do not create worktrees", "copied repositories",
            "branch switches", "would need to create or enter another checkout",
        ]:
            self.assertIn(phrase, self.subagent)

    def test_shared_state_references_are_byte_identical(self):
        contents = [path.resolve().read_bytes() for path in STATE_REFERENCES]
        self.assertTrue(contents)
        self.assertTrue(all(content == contents[0] for content in contents[1:]))


if __name__ == "__main__":
    unittest.main()
