import unittest
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parents[1]


class ExecutionContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skill = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")
        cls.report_template = (
            SKILL_DIR / "references" / "review-report-template.md"
        ).read_text(encoding="utf-8")
        cls.independent_review_path = (
            SKILL_DIR / "references" / "independent-code-review.md"
        )
        cls.independent_review = cls.independent_review_path.read_text(
            encoding="utf-8"
        )

    def test_report_renderer_is_the_canonical_executable_writer(self):
        for phrase in [
            "## Report Renderer Contract",
            "scripts/render_review_report.py",
            "render_review_report.py init",
            "render_review_report.py append",
            "render_review_report.py finalize",
            "renderer fallback",
        ]:
            self.assertIn(phrase, self.skill)

    def test_default_scope_excludes_prizmkit_and_generated_support(self):
        for phrase in [
            "## Default Correctness Scope",
            "Every `.prizmkit/**` path is excluded by default",
            "AGENTS.md",
            "scope-classification",
            "exact default-excluded changed paths",
        ]:
            self.assertIn(phrase, self.skill)

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

    def test_independent_review_follows_main_agent_convergence(self):
        self.assertLess(
            self.skill.index("## Phase 1: Main-Agent Review Loop"),
            self.skill.index("## Phase 3: Independent Code Review"),
        )
        required = [
            "only after the Main-Agent review and repair loop converges",
            "independent-code-review.md",
            "maximum five Reviewer responses",
            "Main-Agent review remains mandatory",
        ]
        for phrase in required:
            self.assertIn(phrase, self.skill)

    def test_each_main_round_starts_from_diff_and_loads_context_on_demand(self):
        required = [
            "current requirement context",
            "git status --short",
            "staged diff",
            "unstaged diff",
            "untracked, deleted, and renamed paths",
            "Reuse current context and load only missing or potentially stale material",
            "Inspect unchanged callers, dependents, contracts, or tests only when",
            "reproducible failure scenario",
        ]
        for phrase in required:
            self.assertIn(phrase, self.skill)

    def test_complete_skill_owned_code_reviewer_prompt(self):
        required = [
            "## Initial Reviewer Prompt",
            "## Resume Prompt",
            "sole independent Code Reviewer",
            "Complete this review personally",
            "Do not create, schedule, resume, continue, request, or coordinate another execution unit",
            "Do not ask the Main Agent to create a helper",
            "Do not modify, create, delete, rename, stage, commit, or otherwise mutate files",
            "Do not execute shell, Git, tests, builds, network calls, external processes",
            "Do not perform unconditional repository discovery or a full repository scan",
            "Do not invent an issue merely to return feedback",
            "Do not expose private reasoning traces",
        ]
        for phrase in required:
            self.assertIn(phrase, self.independent_review)

    def test_strict_semantic_capability_gate(self):
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
            "create no Reviewer",
            "Prompt instructions cannot satisfy",
            "must not branch on platform identity",
        ]
        for phrase in required:
            self.assertIn(phrase, self.independent_review)

    def test_reviewer_uses_complete_current_change_and_exact_identity(self):
        required = [
            "artifact_dir",
            "spec_path",
            "plan_path",
            "checkout_root",
            "staged and unstaged tracked changes",
            "untracked, deleted, and renamed content",
            "concrete coupling",
            "It may use structurally read-only checkout access",
            "REVIEW_BLOCKED",
        ]
        for phrase in required:
            self.assertIn(phrase, self.independent_review)

    def test_minimal_result_protocol_and_adjudication(self):
        for result in (
            "NO_CORRECTION_NEEDED",
            "CORRECTION_NEEDED",
            "REVIEW_BLOCKED",
        ):
            self.assertIn(result, self.independent_review)
        for field in ("- Target:", "- Problem:", "- Evidence:", "- Correction:"):
            self.assertIn(field, self.independent_review)
        for decision in ("accepted", "rejected", "unresolved"):
            self.assertIn(decision, self.independent_review)
        output_protocol = self.independent_review.split(
            "## Reviewer Output Protocol", 1
        )[1].split("## Main-Agent Adjudication", 1)[0]
        for forbidden in ("Severity:", "Confidence:", "Dimension:"):
            self.assertNotIn(forbidden, output_protocol)

    def test_continuation_replacement_and_five_response_budget(self):
        required = [
            "maximum five responses",
            "prefer native continuation",
            "compliant replacement",
            "complete current state",
            "does not reset the five-response budget",
            "At most one replacement may be created in the stage",
            "fifth response",
            "no sixth response",
            "targeted verification",
            "complete final change",
        ]
        for phrase in required:
            self.assertIn(phrase, self.independent_review)

    def test_continuation_failure_uses_replacement_or_local_fallback(self):
        required = [
            "continuation and compliant replacement both fail",
            "Never create a weaker Reviewer",
            "rerun Main-Agent review",
            "record downgrade",
        ]
        for phrase in required:
            self.assertIn(phrase, self.independent_review)

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
            "initialize a replacement report",
            "append",
            "## Final Result",
            "exactly one final result",
            "{artifact_dir}/review-report.md",
        ]
        for phrase in required:
            self.assertIn(phrase, self.skill)
        self.assertNotIn("review-result-state.json", self.skill)

    def test_report_contract_includes_independent_progress_only(self):
        required = [
            "## Independent Review Round <N>",
            "independent-review-round",
            "independent-adjudication",
            "independent-review-downgrade",
            "Final State Independently Rechecked",
        ]
        combined = self.skill + self.report_template
        for phrase in required:
            self.assertIn(phrase, combined)

    def test_review_verdicts_remain_pass_or_needs_fixes(self):
        self.assertIn("PASS | NEEDS_FIXES", self.skill)
        self.assertIn("PASS | NEEDS_FIXES", self.report_template)
        self.assertNotIn(
            "Verdict: <PASS | NEEDS_FIXES | BLOCKED>", self.report_template
        )

    def test_review_is_stage_local_and_returns_domain_verdict_only(self):
        for phrase in [
            "returns `PASS` or `NEEDS_FIXES` and stops",
            "Do not invoke another Skill",
            "Return only the listed review outputs",
        ]:
            self.assertIn(phrase, self.skill)
        for forbidden in [
            "workflow-state.json",
            "workflow-checkpoint.json",
            "next_stage",
            "resume_from",
            "completed_stages",
            "REVIEW_PASS",
            "REVIEW_NEEDS_FIXES",
            "prizmkit-test",
            "prizmkit-implement",
        ]:
            self.assertNotIn(forbidden, self.skill)

    def test_no_platform_role_or_obsolete_execution_protocol_is_required(self):
        self.assertTrue(self.independent_review_path.exists())
        self.assertFalse((SKILL_DIR / "references" / "reviewer-agent-prompt.md").exists())
        self.assertFalse((SKILL_DIR / "assets" / "reviewer-role.json").exists())
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
