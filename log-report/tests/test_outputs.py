import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")

REQUEST_LINE_RE = re.compile(
    r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH|OPTIONS)\s+(\S+)\s+HTTP/\d(?:\.\d)?"'
)


def _ground_truth():
    """Recompute expected stats directly from the log, independent of any
    code under test, so a report that merely echoes a shared bug can't
    pass by coincidence."""
    total = 0
    ips = set()
    paths = Counter()

    for raw_line in LOG_PATH.read_text().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        total += 1
        ips.add(line.split()[0])
        match = REQUEST_LINE_RE.search(line)
        if match:
            paths[match.group(1)] += 1

    top_count = max(paths.values())
    top_paths = {p for p, c in paths.items() if c == top_count}
    return total, len(ips), top_paths


def test_criterion_1_report_exists_and_is_valid_json():
    """instruction.md success criterion 1: /app/report.json exists and
    contains valid JSON."""
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    assert REPORT_PATH.stat().st_size > 0, "report.json is empty"
    try:
        data = json.loads(REPORT_PATH.read_text())
    except json.JSONDecodeError as e:
        raise AssertionError(f"report.json is not valid JSON: {e}")
    assert isinstance(data, dict), "report.json must contain a JSON object"


def test_criterion_2_schema_has_exactly_the_three_keys():
    """instruction.md success criterion 2: the JSON object has exactly the
    keys total_requests, unique_ips, and top_path — no extra, none missing."""
    data = json.loads(REPORT_PATH.read_text())
    expected_keys = {"total_requests", "unique_ips", "top_path"}
    assert set(data.keys()) == expected_keys, (
        f"expected exactly {expected_keys}, got {set(data.keys())}"
    )


def test_criterion_3_total_requests_and_unique_ips_are_exact():
    """instruction.md success criterion 3: total_requests and unique_ips
    exactly match the true counts computed from /app/access.log."""
    data = json.loads(REPORT_PATH.read_text())
    expected_total, expected_unique_ips, _ = _ground_truth()
    assert data["total_requests"] == expected_total, (
        f"total_requests should be {expected_total}, got {data['total_requests']!r}"
    )
    assert data["unique_ips"] == expected_unique_ips, (
        f"unique_ips should be {expected_unique_ips}, got {data['unique_ips']!r}"
    )


def test_criterion_4_top_path_is_a_correct_mode():
    """instruction.md success criterion 4: top_path is a path whose request
    count equals the maximum request count of any path (ties permitted)."""
    data = json.loads(REPORT_PATH.read_text())
    _, _, expected_top_paths = _ground_truth()
    assert data["top_path"] in expected_top_paths, (
        f"top_path should be one of {sorted(expected_top_paths)} "
        f"(tied for most requests), got {data['top_path']!r}"
    )
