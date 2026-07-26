import unittest
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]


class IndependentPlanReviewContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        cls.local_review = (
            SKILL_DIR / "references" / "review-plan-spec-loop.md"
        ).read_text(encoding="utf-8")
        cls.independent_review_path = (
            SKILL_DIR / "references" / "independent-plan-review.md"
        )
        cls.independent_review = cls.independent_review_path.read_text(
            encoding="utf-8"
        )
        cls.plan_template = (SKILL_DIR / "assets" / "plan-template.md").read_text(
            encoding="utf-8"
        )

    def test_independent_review_runs_only_after_local_review_converges(self):
        self.assertLess(
            self.skill.index("## Phase 4: Plan/Spec Review Loop"),
            self.skill.index("## Phase 5: Independent Plan Review"),
        )
        required = [
            "maximum of two planning-review rounds",
            "no unresolved blocker remains",
            "independent-plan-review.md",
            "only after the Main-Agent Plan/Spec review converges",
        ]
        for phrase in required:
            self.assertIn(phrase, self.skill)
        self.assertIn("mandatory Main-Agent baseline", self.local_review)
        self.assertIn("maximum of two", self.local_review)

    def test_reference_contains_the_complete_plan_reviewer_prompt(self):
        required = [
            "## Initial Reviewer Prompt",
            "## Resume Prompt",
            "sole independent Plan Reviewer",
            "Complete this review personally",
            "Do not create, schedule, resume, continue, request, or coordinate another execution unit",
            "Do not ask the Main Agent to create a helper",
            "Do not modify, create, delete, rename, stage, commit, or otherwise mutate files",
            "Do not execute shell, Git, tests, builds, network calls, external processes",
            "Do not inspect implementation code or perform repository discovery",
            "Do not invent an issue merely to return feedback",
            "Do not expose private reasoning traces",
        ]
        for phrase in required:
            self.assertIn(phrase, self.independent_review)

    def test_capability_gate_is_all_or_nothing_and_semantic(self):
        required = [
            "all-or-nothing",
            "read-only",
            "concurrency: at-most-one-active-reviewer",
            "mutation: structurally-unavailable",
            "command_execution: structurally-unavailable",
            "network_access: structurally-unavailable",
            "external_process_execution: structurally-unavailable",
            "downstream_execution: structurally-unavailable",
            "continuation: prefer-same-unit",
            "replacement: compliant-replacement-allowed",
            "model_configuration: inherit-current-session",
            "any capability is missing or cannot be proven",
            "do not create a Reviewer",
            "Prompt instructions cannot satisfy",
            "must not branch on platform identity",
        ]
        for phrase in required:
            self.assertIn(phrase, self.independent_review)

    def test_input_has_exact_identity_and_planning_only_scope(self):
        required = [
            "artifact_dir",
            "spec_path",
            "plan_path",
            "original requirement and confirmed clarifications",
            "The Plan Reviewer receives only",
            "does not receive or inspect implementation diffs",
            "REVIEW_BLOCKED",
        ]
        for phrase in required:
            self.assertIn(phrase, self.independent_review)

    def test_minimal_result_protocol_has_no_extra_finding_taxonomy(self):
        for result in (
            "NO_CORRECTION_NEEDED",
            "CORRECTION_NEEDED",
            "REVIEW_BLOCKED",
        ):
            self.assertIn(result, self.independent_review)
        for field in ("- Target:", "- Problem:", "- Evidence:", "- Correction:"):
            self.assertIn(field, self.independent_review)
        output_protocol = self.independent_review.split(
            "## Reviewer Output Protocol", 1
        )[1].split("## Main-Agent Adjudication", 1)[0]
        for forbidden in ("Severity:", "Confidence:", "Dimension:"):
            self.assertNotIn(forbidden, output_protocol)

    def test_main_agent_adjudicates_and_retains_mutation_authority(self):
        required = [
            "accepted",
            "rejected",
            "unresolved",
            "Main Agent",
            "modifies `spec.md` and/or `plan.md`",
            "PLAN_BLOCKED",
        ]
        for phrase in required:
            self.assertIn(phrase, self.independent_review)

    def test_continuation_replacement_and_two_response_budget(self):
        required = [
            "maximum two responses",
            "prefer native continuation",
            "compliant replacement",
            "complete current content",
            "does not reset the two-response budget",
            "At most one replacement may be created in the stage",
            "second response",
            "no third response",
            "targeted Plan/Spec verification",
        ]
        for phrase in required:
            self.assertIn(phrase, self.independent_review)
        self.assertIn("maximum two Reviewer responses", self.skill)

    def test_strict_downgrade_preserves_completed_local_review(self):
        required = [
            "Strict Downgrade",
            "no Reviewer is created",
            "record the downgrade",
            "completed Main-Agent review",
            "continuation and compliant replacement both fail",
            "Never create a weaker Reviewer",
            "rerun the local Plan/Spec review",
        ]
        for phrase in required:
            self.assertIn(phrase, self.independent_review)

    def test_plan_template_has_terminal_independent_review_record(self):
        required = [
            "## Independent Plan Review",
            "Capability Gate: <ENABLED | DOWNGRADED>",
            "Reviewer Responses: <0..2>",
            "Continuation Mode: <native | replacement | mixed | not-applicable>",
            "Reviewer Replacements: <0..1>",
            "Final State Independently Rechecked: <yes | no | not applicable>",
            "### Adjudication",
            "Decision: <accepted | rejected | unresolved>",
            "Appending this terminal record does not trigger another Reviewer response",
        ]
        for phrase in required:
            self.assertIn(phrase, self.plan_template)

    def test_lifecycle_results_remain_plan_ready_or_plan_blocked(self):
        self.assertIn("PLAN_READY", self.skill)
        self.assertIn("PLAN_BLOCKED", self.skill)
        self.assertNotIn("INDEPENDENT_REVIEW_PASS", self.skill)
        self.assertNotIn("INDEPENDENT_REVIEW_BLOCKED", self.skill)


if __name__ == "__main__":
    unittest.main()
