import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]
ATOMIC_SKILLS = {
    "plan": (SKILL_DIR / "../prizmkit-plan").resolve(),
    "implement": (SKILL_DIR / "../prizmkit-implement").resolve(),
    "code-review": (SKILL_DIR / "../prizmkit-code-review").resolve(),
    "test": (SKILL_DIR / "../prizmkit-test").resolve(),
    "retrospective": (SKILL_DIR / "../prizmkit-retrospective").resolve(),
    "committer": (SKILL_DIR / "../prizmkit-committer").resolve(),
}


class WorkflowContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        cls.state = (SKILL_DIR / "references" / "workflow-state-protocol.md").read_text(
            encoding="utf-8"
        )
        cls.atomic_skills = {
            name: (directory / "SKILL.md").read_text(encoding="utf-8")
            for name, directory in ATOMIC_SKILLS.items()
        }
        cls.atomic_content = {
            name: "\n".join(
                path.read_text(encoding="utf-8")
                for path in sorted(directory.rglob("*.md"))
                if "tests" not in path.parts
            )
            for name, directory in ATOMIC_SKILLS.items()
        }
        cls.subagent = (
            ATOMIC_SKILLS["implement"]
            / "references"
            / "implementation-subagent-procedure.md"
        ).read_text(encoding="utf-8")

    def test_composite_coordinates_exactly_six_mandatory_stages_in_order(self):
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
        self.assertIn("The six stages are mandatory", self.skill)

    def test_composite_owns_artifact_identity_state_and_routing(self):
        for phrase in [
            "same `artifact_dir`",
            ".prizmkit/state/workflows/<requirement-identity>.json",
            ".prizmkit/specs/<requirement-slug>/",
            ".prizmkit/bugfix/<bug-id>/",
            ".prizmkit/refactor/<refactor-id>/",
            "external host execution checkpoint",
            "Never select a different most-recent plan",
            "Validate those artifacts independently",
            "Map the domain result",
        ]:
            self.assertIn(phrase, self.skill)
        self.assertIn("External host checkpoint", self.state)
        identity = (SKILL_DIR / "references" / "artifact-identity.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("final path component unchanged", identity)
        self.assertIn("naming collision with a different artifact directory is blocking", identity)
        self.assertIn("never generates a second slug", identity)

    def test_composite_state_maps_stage_results(self):
        for field in [
            '"artifact_dir"',
            '"stage"',
            '"status"',
            '"stage_result"',
            '"completed_stages"',
            '"repair_scope"',
            '"repair_round"',
            '"next_stage"',
            '"resume_from"',
        ]:
            self.assertIn(field, self.state)
        for result in [
            "PLAN_READY",
            "IMPLEMENTED",
            "REVIEW_PASS",
            "REVIEW_NEEDS_FIXES",
            "TEST_PASS",
            "TEST_NEEDS_FIXES",
            "TEST_BLOCKED",
            "RETRO_COMPLETE",
            "COMMITTED",
        ]:
            self.assertIn(result, self.state)

    def test_atomic_skill_trees_have_no_caller_state_protocol(self):
        forbidden = [
            "workflow-state.json",
            "workflow-checkpoint.json",
            ".prizmkit/state/workflows",
            "next_stage",
            "resume_from",
            "completed_stages",
            "COMMIT_PENDING",
            "WORKFLOW_COMPLETED",
            "WORKFLOW_BLOCKED",
            "orchestrator",
            "handoff",
        ]
        for name, content in self.atomic_content.items():
            for phrase in forbidden:
                self.assertNotIn(phrase, content, f"{name} exposes {phrase}")
            self.assertFalse(
                (ATOMIC_SKILLS[name] / "references" / "workflow-state-protocol.md").exists(),
                f"{name} carries a copied caller-state protocol",
            )

    def test_atomic_skills_do_not_name_or_invoke_sibling_stages(self):
        skill_names = {
            name: f"prizmkit-{name}" for name in ATOMIC_SKILLS
        }
        for name, content in self.atomic_content.items():
            for sibling, command in skill_names.items():
                if sibling != name:
                    self.assertNotIn(command, content, f"{name} names sibling {command}")

    def test_atomic_skills_return_only_stage_local_results(self):
        expected = {
            "plan": ("PLAN_READY", "PLAN_BLOCKED"),
            "implement": ("IMPLEMENTED", "IMPLEMENT_BLOCKED"),
            "code-review": ("PASS", "NEEDS_FIXES"),
            "test": ("TEST_PASS", "TEST_NEEDS_FIXES", "TEST_BLOCKED"),
            "retrospective": ("RETRO_COMPLETE", "RETRO_BLOCKED"),
            "committer": ("COMMIT_REQUEST_READY", "COMMIT_BLOCKED"),
        }
        for name, results in expected.items():
            for result in results:
                self.assertIn(result, self.atomic_skills[name])

    def test_passing_test_production_change_routes_through_delta_review(self):
        for phrase in [
            "production_changed=true",
            "production_changed=false",
            "review_scope=delta",
            "clear stale stage_result",
            "repair_round < 3",
            "fresh prizmkit-test",
        ]:
            self.assertIn(phrase, self.skill + self.state)

    def test_test_skill_keeps_only_its_internal_bounded_loops(self):
        test = self.atomic_skills["test"]
        self.assertIn("Use at most ten completed rounds", test)
        self.assertIn("at most five responses", test)
        self.assertIn("Use at most three execution-failure repair rounds", test)
        self.assertIn("After writing its result, this Skill stops", test)

    def test_commit_operations_remain_separate(self):
        committer = self.atomic_skills["committer"]
        for phrase in [
            "operation=interactive-commit",
            "operation=prepare-runtime-commit",
            "COMMIT_REQUEST_READY",
            "The Python Runtime independently revalidates exact changed/staged/committed sets",
            "Remote publication is outside this Skill",
        ]:
            self.assertIn(phrase, committer)
        for phrase in [
            "exact `intended_paths`",
            "regardless of whether a justified path is under `.prizmkit/**`",
            "External headless orchestration supplies explicit readiness evidence",
            "support_validation_evidence",
            "User confirmation alone is not support validation",
        ]:
            self.assertIn(phrase, self.skill)
        self.assertNotIn("local_commit_authorized", committer)
        self.assertNotIn("COMMIT_PENDING", committer)
        self.assertIn("atomic operation result `COMMIT_DECLINED`", self.skill)
        self.assertIn("`COMMIT_PENDING` is reserved for a validated Runtime commit request", self.skill)

    def test_implementation_subagent_checkout_boundary_is_unchanged(self):
        for phrase in [
            "same active checkout",
            "Do not create worktrees",
            "copied repositories",
            "branch switches",
            "would need to create or enter another checkout",
        ]:
            self.assertIn(phrase, self.subagent)


if __name__ == "__main__":
    unittest.main()
