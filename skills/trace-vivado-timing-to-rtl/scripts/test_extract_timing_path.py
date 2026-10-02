"""Exercise the report extractor CLI with small synthetic timing reports."""

from __future__ import annotations

import csv
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).with_name("extract_timing_path.py").resolve()

# All names and numbers are synthetic. The launch clock adds 3 ns to the
# absolute path column; the extracted data path itself is exactly 1 ns.
DATA_ROWS = """\
    SLICE_X1Y1 FDRE (Prop_fdre_C_Q) 0.100 3.100 r top/launch/Q
    net (fo=4, routed) 0.200 3.300 top/launch_net
    SLICE_X2Y2 LUT2 (Prop_lut2_I0_O)
                                  0.150 3.450 f top/logic/O
    net (fo=12, estimated) 0.250 3.700 top/logic_net
    SLICE_X3Y3 CARRY4 (Prop_carry4_CI_CO) 0.300 4.000 r top/carry/CO[3]
"""


def report_path(
    source: str = "top/launch_a/Q",
    destination: str = "top/sink_a/D",
    status: str = "VIOLATED",
    slack: str = "-0.125",
    rows: str = DATA_ROWS,
) -> str:
    return f"""\
Slack ({status}) : {slack}ns
  Source: {source}
  Destination: {destination}
  Requirement: 12.500ns
  Data Path Delay: 1.000ns (logic 0.550ns (55.000%) route 0.450ns (45.000%))
  Logic Levels: 2 (CARRY4=1 LUT2=1)

  Location             Delay type                 Incr(ns) Path(ns) Netlist Resource(s)
  ----------------------------------------------------------------------------------
    BUFGCTRL_X0Y0 BUFG (Prop_bufg_I_O) 0.200 3.000 r clock/launch/O
    net (fo=100, routed) 0.000 3.000 clock/launch_net
  ----------------------------------------------------------------------------------
{rows}  ----------------------------------------------------------------------------------
    BUFGCTRL_X0Y1 BUFG (Prop_bufg_I_O) 0.250 15.500 r clock/capture/O
    net (fo=200, routed) 0.100 15.600 clock/capture_net
"""


MULTI_PATH_REPORT = (
    report_path()
    + report_path("top/launch_b/Q", "top/sink_a/D", "MET", "0.250")
    + report_path("top/launch_a/Q", "top/sink_b/D", "MET", "0.500")
)


class ExtractTimingPathTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.report = self.directory / "timing report.rpt"
        self.report.write_text(report_path(), encoding="utf-8")

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-B", "-X", "utf8", str(SCRIPT), str(self.report), *args],
            cwd=self.directory,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding="utf-8",
            check=False,
            timeout=15,
        )

    def json_result(self, *args: str) -> dict:
        completed = self.run_cli("--format", "json", *args)
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stderr, "")
        return json.loads(completed.stdout)

    def assert_cli_error(self, code: int, message: str, *args: str) -> None:
        completed = self.run_cli(*args)
        self.assertEqual(completed.returncode, code, completed.stderr)
        self.assertEqual(completed.stdout, "")
        self.assertIn(message, completed.stderr)
        self.assertNotIn("Traceback", completed.stderr)

    def test_json_parses_metadata_and_inline_and_wrapped_primitives(self) -> None:
        path = self.json_result()
        self.assertEqual(path["status"], "VIOLATED")
        self.assertEqual(path["slack_ns"], -0.125)
        self.assertEqual(path["source"], "top/launch_a/Q")
        self.assertEqual(path["destination"], "top/sink_a/D")
        self.assertEqual(path["requirement_ns"], 12.5)
        self.assertEqual(path["data_path_delay_ns"], 1.0)
        self.assertEqual(path["logic_delay_ns"], 0.55)
        self.assertEqual(path["route_delay_ns"], 0.45)
        self.assertEqual(path["logic_levels"], 2)
        self.assertEqual(path["primitive_counts"], "CARRY4=1 LUT2=1")
        stages = path["stages"]
        self.assertEqual([stage["index"] for stage in stages], [0, 1, 2])
        self.assertEqual([stage["primitive"] for stage in stages], ["FDRE", "LUT2", "CARRY4"])
        self.assertEqual([stage["site"] for stage in stages], ["SLICE_X1Y1", "SLICE_X2Y2", "SLICE_X3Y3"])
        self.assertEqual(stages[1]["arc"], "Prop_lut2_I0_O")
        self.assertEqual(stages[1]["cell_resource"], "top/logic/O")
        self.assertEqual([stage["cell_delay_ns"] for stage in stages], [0.1, 0.15, 0.3])

    def test_following_nets_belong_to_the_preceding_primitive(self) -> None:
        stages = self.json_result()["stages"]
        self.assertEqual([stage["following_net"] for stage in stages], ["top/launch_net", "top/logic_net", ""])
        self.assertEqual([stage["fanout"] for stage in stages], [4, 12, None])
        self.assertEqual([stage["route_state"] for stage in stages], ["routed", "estimated", ""])
        self.assertEqual([stage["route_delay_ns"] for stage in stages], [0.2, 0.25, 0.0])

    def test_zero_fanout_remains_distinct_from_a_missing_net(self) -> None:
        self.report.write_text(report_path().replace("fo=4", "fo=0"), encoding="utf-8")
        stages = self.json_result()["stages"]
        self.assertEqual(stages[0]["fanout"], 0)
        self.assertIsNone(stages[2]["fanout"])
        completed = self.run_cli()
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("| 0 | 0.300 |  | measured |", completed.stdout)

    def test_cumulative_delays_exclude_launch_clock_and_end_without_a_net(self) -> None:
        stages = self.json_result()["stages"]
        for stage, after_cell, after_route in zip(stages, [0.1, 0.45, 1.0], [0.3, 0.7, 1.0]):
            with self.subTest(stage=stage["index"]):
                self.assertAlmostEqual(stage["cumulative_after_cell_ns"], after_cell)
                self.assertAlmostEqual(stage["cumulative_after_route_ns"], after_route)
        self.assertNotIn("clock/", json.dumps(stages))

    def test_optional_metadata_is_null_when_absent(self) -> None:
        text = report_path()
        text = "\n".join(
            line for line in text.splitlines()
            if not line.strip().startswith(("Requirement:", "Data Path Delay:", "Logic Levels:"))
        )
        self.report.write_text(text, encoding="utf-8")
        path = self.json_result()
        for field in ("requirement_ns", "data_path_delay_ns", "logic_delay_ns", "route_delay_ns", "logic_levels"):
            with self.subTest(field=field):
                self.assertIsNone(path[field])
        self.assertEqual(path["primitive_counts"], "")
        self.assertEqual(len(path["stages"]), 3)

    def test_path_index_is_zero_based_and_preserves_report_order(self) -> None:
        self.report.write_text(MULTI_PATH_REPORT, encoding="utf-8")
        self.assertEqual(self.json_result()["slack_ns"], -0.125)
        for index, slack in ((0, -0.125), (1, 0.25), (2, 0.5)):
            with self.subTest(index=index):
                self.assertEqual(self.json_result("--path-index", str(index))["slack_ns"], slack)

    def test_source_and_destination_filters_match_substrings(self) -> None:
        self.report.write_text(MULTI_PATH_REPORT, encoding="utf-8")
        self.assertEqual(self.json_result("--source", "launch_b")["slack_ns"], 0.25)
        self.assertEqual(self.json_result("--destination", "sink_b")["slack_ns"], 0.5)
        selected = self.json_result("--source", "launch_a", "--destination", "sink_b")
        self.assertEqual((selected["source"], selected["destination"]), ("top/launch_a/Q", "top/sink_b/D"))

    def test_path_index_is_applied_after_filtering(self) -> None:
        self.report.write_text(MULTI_PATH_REPORT, encoding="utf-8")
        selected = self.json_result("--source", "launch_a", "--path-index", "1")
        self.assertEqual(selected["destination"], "top/sink_b/D")
        self.assert_cli_error(2, "outside 0..1", "--source", "launch_a", "--path-index", "2")

    def test_unmatched_source_destination_or_combination_returns_two(self) -> None:
        self.report.write_text(MULTI_PATH_REPORT, encoding="utf-8")
        for args in (
            ("--source", "missing"),
            ("--source", "LAUNCH_A"),
            ("--destination", "missing"),
            ("--source", "launch_b", "--destination", "sink_b"),
            ("--list", "--source", "missing"),
        ):
            with self.subTest(args=args):
                self.assert_cli_error(2, "no timing path matched", *args)

    def test_report_without_timing_blocks_returns_two(self) -> None:
        for text in ("", "Timing analysis completed; no timing paths.\n"):
            with self.subTest(text=text):
                self.report.write_text(text, encoding="utf-8")
                self.assert_cli_error(2, "no timing path matched")

    def test_negative_and_out_of_range_indices_return_two(self) -> None:
        self.report.write_text(MULTI_PATH_REPORT, encoding="utf-8")
        for index in ("-1", "3"):
            with self.subTest(index=index):
                self.assert_cli_error(2, f"path index {index} is outside 0..2", "--path-index", index)

    def test_path_without_parsed_data_stages_returns_three(self) -> None:
        for text in (
            report_path(rows=""),
            report_path(rows="    unrecognized data row\n"),
            "Slack (MET) : 0.100ns\n  Source: top/a/Q\n  Destination: top/b/D\n" + DATA_ROWS,
        ):
            with self.subTest(report=text):
                self.report.write_text(text, encoding="utf-8")
                self.assert_cli_error(3, "selected path has no parsed data-path stages")

    def test_markdown_is_the_default_and_escapes_table_pipes(self) -> None:
        self.report.write_text(report_path().replace("top/logic/O", "top/logic|wide/O"), encoding="utf-8")
        completed = self.run_cli()
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stderr, "")
        self.assertTrue(completed.stdout.startswith("## Timing path\n"))
        self.assertIn("- Slack: `-0.125 ns`", completed.stdout)
        self.assertIn("- Data/Logic/Route: `1.000/0.550/0.450 ns`", completed.stdout)
        self.assertIn("`top/logic\\|wide/O`", completed.stdout)
        self.assertIn("| 12 | 0.700 |  | measured |", completed.stdout)
        self.assertIn("|  | 1.000 |  | measured |", completed.stdout)
        self.assertNotIn("clock/", completed.stdout)

    def test_csv_preserves_fields_and_quoted_resource_names(self) -> None:
        resource = 'top/data,"selected"/O'
        self.report.write_text(report_path().replace("top/logic/O", resource), encoding="utf-8")
        completed = self.run_cli("--format", "csv")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stderr, "")
        rows = list(csv.DictReader(io.StringIO(completed.stdout)))
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[1]["cell_resource"], resource)
        self.assertEqual(rows[1]["primitive"], "LUT2")
        self.assertEqual(rows[1]["fanout"], "12")
        self.assertAlmostEqual(float(rows[1]["cumulative_after_route_ns"]), 0.7)
        self.assertEqual(rows[2]["fanout"], "")
        self.assertEqual(rows[2]["following_net"], "")

    def test_output_files_match_stdout_for_every_format(self) -> None:
        self.report.write_text(report_path(source="top/合成寄存器/Q"), encoding="utf-8")
        for output_format in ("markdown", "csv", "json"):
            with self.subTest(output_format=output_format):
                expected = self.run_cli("--format", output_format)
                output = self.directory / f"提取结果 {output_format}.txt"
                completed = self.run_cli("--format", output_format, "--output", str(output))
                self.assertEqual(expected.returncode, 0, expected.stderr)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                self.assertEqual(completed.stderr, "")
                self.assertEqual(completed.stdout, "")
                self.assertEqual(output.read_text(encoding="utf-8"), expected.stdout)

    def test_failed_selection_does_not_overwrite_output_file(self) -> None:
        output = self.directory / "result.json"
        for report, args, code, message in (
            (report_path(), ("--source", "missing"), 2, "no timing path matched"),
            (report_path(), ("--path-index", "1"), 2, "outside 0..0"),
            (report_path(rows=""), (), 3, "no parsed data-path stages"),
        ):
            with self.subTest(args=args, code=code):
                self.report.write_text(report, encoding="utf-8")
                output.write_text("existing result\n", encoding="utf-8")
                self.assert_cli_error(code, message, *args, "--output", str(output))
                self.assertEqual(output.read_text(encoding="utf-8"), "existing result\n")

    def test_list_summarizes_all_filtered_paths_in_markdown(self) -> None:
        self.report.write_text(MULTI_PATH_REPORT, encoding="utf-8")
        completed = self.run_cli("--list", "--source", "launch_a", "--format", "json", "--path-index", "99")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stderr, "")
        lines = completed.stdout.splitlines()
        self.assertEqual(len(lines), 4)
        self.assertEqual(lines[0], "| Index | Status | Slack ns | Data ns | Levels | Source | Destination |")
        self.assertEqual(lines[2], "| 0 | VIOLATED | -0.125 | 1.000 | 2 | `top/launch_a/Q` | `top/sink_a/D` |")
        self.assertEqual(lines[3], "| 1 | MET | 0.500 | 1.000 | 2 | `top/launch_a/Q` | `top/sink_b/D` |")

    def test_list_preserves_zero_logic_levels(self) -> None:
        text = report_path(rows="\n".join(DATA_ROWS.splitlines()[:2]) + "\n")
        text = text.replace("Logic Levels: 2 (CARRY4=1 LUT2=1)", "Logic Levels: 0 ()")
        text = text.replace(
            "1.000ns (logic 0.550ns (55.000%) route 0.450ns (45.000%))",
            "0.300ns (logic 0.100ns (33.333%) route 0.200ns (66.667%))",
        )
        self.report.write_text(text, encoding="utf-8")
        self.assertEqual(self.json_result()["logic_levels"], 0)
        completed = self.run_cli("--list")
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stderr, "")
        self.assertIn("| -0.125 | 0.300 | 0 | `top/launch_a/Q` |", completed.stdout)

    def test_list_allows_unparsed_stages_and_writes_output(self) -> None:
        self.report.write_text(report_path(source="top/a|b/Q", rows=""), encoding="utf-8")
        output = self.directory / "summary.md"
        completed = self.run_cli("--list", "--output", str(output))
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout, "")
        self.assertEqual(completed.stderr, "")
        text = output.read_text(encoding="utf-8")
        self.assertIn("| 0 | VIOLATED | -0.125 |", text)
        self.assertIn("`top/a\\|b/Q`", text)


if __name__ == "__main__":
    unittest.main()
