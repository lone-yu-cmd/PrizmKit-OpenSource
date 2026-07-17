import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

import render_review_report  # noqa: E402


class ReportLifecycleTests(unittest.TestCase):
    def _pass_result(self):
        return {
            "verdict": "PASS",
            "main_review_rounds": 2,
            "accepted_findings": 1,
            "fixed_findings": 1,
            "rejected_findings": 0,
            "unresolved_findings": 0,
            "summary": "Review converged.",
        }

    def test_initialize_replaces_stale_report(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "review-report.md"
            report.write_text("## Final Result\n- Verdict: PASS\n")
            render_review_report.initialize_report(report)
            text = report.read_text()
            self.assertIn("## Status: IN_PROGRESS", text)
            self.assertNotIn("## Final Result", text)

    def test_append_preserves_prior_sections(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "review-report.md"
            render_review_report.initialize_report(report)
            render_review_report.append_event(
                report,
                {
                    "event": "main-review-round",
                    "round": 1,
                    "findings": 1,
                    "accepted": 1,
                    "rejected": 0,
                    "unresolved": 0,
                    "next": "Repair accepted finding",
                },
            )
            render_review_report.append_event(
                report,
                {
                    "event": "repair-verification",
                    "fixed_findings": 1,
                    "verification": "Targeted test passed.",
                    "next": "Main Review Round 2",
                },
            )
            text = report.read_text()
            self.assertLess(text.index("## Main Review Round 1"), text.index("## Repair Verification"))

    def test_round_counts_must_include_unresolved_findings(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "review-report.md"
            render_review_report.initialize_report(report)
            with self.assertRaises(render_review_report.ReportStateError):
                render_review_report.append_event(
                    report,
                    {
                        "event": "main-review-round",
                        "round": 1,
                        "findings": 1,
                        "accepted": 0,
                        "rejected": 0,
                        "unresolved": 0,
                        "next": "Invalid",
                    },
                )

    def test_finalize_appends_exactly_one_final_result(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "review-report.md"
            render_review_report.initialize_report(report)
            render_review_report.append_final_result(report, self._pass_result())
            text = report.read_text()
            self.assertEqual(1, text.count("## Final Result"))
            self.assertIn("- Verdict: PASS", text)
            with self.assertRaises(render_review_report.ReportStateError):
                render_review_report.append_final_result(report, self._pass_result())

    def test_append_after_final_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "review-report.md"
            render_review_report.initialize_report(report)
            render_review_report.append_final_result(report, self._pass_result())
            with self.assertRaises(render_review_report.ReportStateError):
                render_review_report.append_event(
                    report,
                    {
                        "event": "final-verification",
                        "status": "COMPLETED",
                        "evidence": "Too late.",
                    },
                )

    def test_needs_fixes_requires_unfixed_or_unresolved_findings(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "review-report.md"
            render_review_report.initialize_report(report)
            invalid = {**self._pass_result(), "verdict": "NEEDS_FIXES"}
            with self.assertRaises(render_review_report.ReportStateError):
                render_review_report.append_final_result(report, invalid)

            valid = {
                **invalid,
                "unresolved_findings": 1,
                "summary": "Required verification environment is unavailable.",
            }
            render_review_report.append_final_result(report, valid)
            self.assertIn("- Verdict: NEEDS_FIXES", report.read_text())

    def test_round_ten_unfixed_accepted_finding_can_need_fixes(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "review-report.md"
            render_review_report.initialize_report(report)
            result = {
                **self._pass_result(),
                "verdict": "NEEDS_FIXES",
                "main_review_rounds": 10,
                "fixed_findings": 0,
                "summary": "Round ten did not converge.",
            }
            render_review_report.append_final_result(report, result)
            self.assertIn("- Verdict: NEEDS_FIXES", report.read_text())

    def test_blocked_is_not_a_review_verdict(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "review-report.md"
            render_review_report.initialize_report(report)
            blocked = {
                **self._pass_result(),
                "verdict": "BLOCKED",
                "unresolved_findings": 1,
            }
            with self.assertRaises(render_review_report.ReportStateError):
                render_review_report.append_final_result(report, blocked)

    def test_in_progress_report_has_no_terminal_verdict(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "review-report.md"
            render_review_report.initialize_report(report)
            render_review_report.append_event(
                report,
                {
                    "event": "main-review-round",
                    "round": 1,
                    "findings": 0,
                    "accepted": 0,
                    "rejected": 0,
                    "unresolved": 0,
                    "next": "Final verification",
                },
            )
            text = report.read_text()
            self.assertIn("## Status: IN_PROGRESS", text)
            self.assertNotIn("- Verdict:", text)

    def test_cli_supports_init_append_and_finalize(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "review-report.md"
            script = str(SCRIPT_DIR / "render_review_report.py")
            subprocess.run([sys.executable, script, "init", str(report)], check=True)
            event = json.dumps(
                {
                    "event": "main-review-round",
                    "round": 1,
                    "findings": 0,
                    "accepted": 0,
                    "rejected": 0,
                    "unresolved": 0,
                    "next": "Final verification",
                }
            )
            subprocess.run(
                [sys.executable, script, "append", str(report)],
                input=event,
                text=True,
                check=True,
            )
            subprocess.run(
                [sys.executable, script, "finalize", str(report)],
                input=json.dumps(self._pass_result()),
                text=True,
                check=True,
            )
            self.assertIn("- Verdict: PASS", report.read_text())


if __name__ == "__main__":
    unittest.main()
