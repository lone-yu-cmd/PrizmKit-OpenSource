import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]


class ExecutionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_DIR / "SKILL.md").read_text()
        cls.report_template = (
            SKILL_DIR / "references" / "review-report-template.md"
        ).read_text()

    def test_main_agent_owns_the_bounded_review_and_repair_loop(self):
        required = [
            "Main-Agent Review Loop",
            "accepted = 0",
            "ten completed review rounds",
            "Main Agent directly repairs",
            "review converged",
        ]
        for phrase in required:
            self.assertIn(phrase, self.skill)

    def test_each_round_reviews_the_complete_current_change(self):
        required = [
            "staged and unstaged tracked changes",
            "untracked files",
            "deleted and renamed files",
            "callers, dependents, contracts, and tests",
            "reproducible failure scenario",
        ]
        for phrase in required:
            self.assertIn(phrase, self.skill)

    def test_missing_evidence_and_unsafe_repairs_become_unresolved(self):
        required = [
            "Missing tools, permissions, environment, or required evidence",
            "unresolved finding",
            "repair cannot be completed safely",
            "NEEDS_FIXES",
        ]
        for phrase in required:
            self.assertIn(phrase, self.skill)

    def test_report_rebuilds_per_execution_then_appends_progress(self):
        required = [
            "replace any prior report",
            "append",
            "## Final Result",
            "exactly one final result",
            "{artifact_dir}/review-report.md",
        ]
        for phrase in required:
            self.assertIn(phrase, self.skill)
        self.assertNotIn("review-result-state.json", self.skill)

    def test_code_review_forbids_direct_indirect_and_nested_review_delegation(self):
        required = [
            "The current Main Agent is the only Code Review executor",
            "Do not delegate any part of Code Review directly or indirectly",
            "Do not invoke another review skill or review workflow",
            "finder, verifier, audit, compatibility review, verification, or gap sweep",
            "review-report.md` is the only persisted review artifact",
        ]
        for phrase in required:
            self.assertIn(phrase, self.skill)

    def test_code_review_has_no_reviewer_execution_mechanism(self):
        forbidden = [
            "Independent Reviewer",
            "semantic risk",
            "low: 0",
            "medium: 1",
            "high: 2",
            "Reviewer 2",
            "Reviewer 3",
            "isolated worktree",
            "infrastructure retry",
            "reviewer-agent-prompt.md",
            "reviewer-role.json",
        ]
        for phrase in forbidden:
            self.assertNotIn(phrase, self.skill)
            self.assertNotIn(phrase, self.report_template)

    def test_review_verdicts_remain_pass_or_needs_fixes(self):
        self.assertIn("PASS | NEEDS_FIXES", self.skill)
        self.assertIn("PASS | NEEDS_FIXES", self.report_template)
        self.assertNotIn("Verdict: <PASS | NEEDS_FIXES | BLOCKED>", self.report_template)

    def test_review_precedes_full_test_and_pass_hands_off_to_test(self):
        required = [
            "before the full test stage",
            "final test evidence represents the final reviewed workspace",
            '"status": "REVIEW_PASS"',
            '"next_stage": "test"',
            '"resume_from": "prizmkit-test"',
            "REVIEW_PASS\n  → /prizmkit-test",
        ]
        for phrase in required:
            self.assertIn(phrase, self.skill)

    def test_review_needs_fixes_routes_to_implementation(self):
        required = [
            '"status": "REVIEW_NEEDS_FIXES"',
            '"repair_scope": "production"',
            '"next_stage": "implement"',
            '"resume_from": "prizmkit-implement"',
            "at most three repair rounds",
        ]
        for phrase in required:
            self.assertIn(phrase, self.skill)

    def test_reviewer_prompt_and_role_are_removed(self):
        self.assertFalse((SKILL_DIR / "references" / "reviewer-agent-prompt.md").exists())
        self.assertFalse((SKILL_DIR / "assets" / "reviewer-role.json").exists())

    def test_obsolete_protocol_files_are_removed(self):
        obsolete = [
            "references/reviewer-execution-protocol.md",
            "references/reviewer-workspace-protocol.md",
            "scripts/check_loop.py",
            "scripts/workspace_snapshot.py",
        ]
        for relative_path in obsolete:
            self.assertFalse((SKILL_DIR / relative_path).exists(), relative_path)


if __name__ == "__main__":
    unittest.main()
