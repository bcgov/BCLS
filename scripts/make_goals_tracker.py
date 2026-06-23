#!/usr/bin/env python3
"""Generate mock tracking data for Look West goals.

Reads ``data/LW Goals.csv`` (which defines, per goal, up to three metric names
plus their data-availability and source) and writes a long-format tracking log
``data/Goals Tracker.csv``.

Schema (long / tracking-log):
    Goal ID, Metric #, Metric Name, Metric Value, Unit, Period, Status,
    Narrative, Source

Row types:
  * Metric rows  -> Metric # in {1,2,3}; carry a value/unit for a period.
  * Summary rows -> Metric # = "Summary"; carry the goal-level Status and
                    Narrative for the latest period (no metric value).

Availability handling (drives the "no data" demonstration):
  * "Uncertain" or blank availability  -> metric is NOT tracked (no rows), so
    the goal card simply omits it.
  * "Partially Available"              -> only the latest period is populated.
  * "Available" (anything else)        -> both periods populated.
"""
import csv
import os
import random

SRC = os.path.join("data", "LW Goals.csv")
OUT = os.path.join("data", "Goals Tracker.csv")

PERIODS = ["2025-Q4", "2026-Q1"]
LATEST = PERIODS[-1]
STATUSES = ["On Track", "On Track", "Early Stage", "At Risk", "Advanced", "Complete"]

HEADERS = [
    "Goal ID", "Metric #", "Metric Name", "Metric Value", "Unit",
    "Period", "Status", "Narrative", "Source",
]


def metric_kind(name):
    n = name.lower()
    if "(y/n" in n or "yes/no" in n or "(y/n)" in n or "(yes/no)" in n:
        return "bool"
    if "%" in name or "percentage" in n:
        return "pct"
    if "$" in name:
        return "money"
    if "(days)" in n:
        return "days"
    return "count"


def has_data(avail):
    a = (avail or "").strip().lower()
    if not a:
        return False
    if a.startswith("uncertain") or a.startswith("not available") or a == "tbd":
        return False
    return True


def both_periods(avail):
    return (avail or "").strip().lower().startswith("available")


def gen_count(rng):
    scale = rng.choice([10, 50, 100, 1000, 5000])
    base = rng.randint(1, 9) * (scale // 10 or 1)
    return base


def gen_series(kind, rng):
    """Return {period: (value_str, unit)} for both PERIODS, with sensible,
    non-regressing movement (counts/$ grow, timelines shrink, Y/N only No->Yes)."""
    p0, p1 = PERIODS
    if kind == "bool":
        progressed = rng.random() < 0.45
        if progressed:
            return {p0: ("No", "Y/N"), p1: ("Yes", "Y/N")}
        val = rng.choice(["Yes", "No", "Yes"])
        return {p0: (val, "Y/N"), p1: (val, "Y/N")}
    if kind == "pct":
        base = round(rng.uniform(5, 80), 1)
        later = round(min(99.0, base + rng.uniform(1, 12)), 1)
        return {p0: (str(base), "%"), p1: (str(later), "%")}
    if kind == "money":
        base = gen_count(rng)
        later = int(base * (1 + rng.uniform(0.05, 0.4)))
        return {p0: (str(base), "$M"), p1: (str(later), "$M")}
    if kind == "days":
        base = rng.randint(180, 680)
        later = max(60, int(base * (1 - rng.uniform(0.05, 0.35))))
        return {p0: (str(base), "days"), p1: (str(later), "days")}
    base = gen_count(rng)
    later = int(base * (1 + rng.uniform(0.05, 0.5)))
    return {p0: (str(base), "#"), p1: (str(later), "#")}


def short_goal(text):
    t = (text or "").strip().rstrip(".")
    if len(t) > 90:
        t = t[:87].rstrip() + "..."
    return t


def make_narrative(goal_text, target, status, primary_name, primary_latest, rng):
    g = short_goal(goal_text)
    bits = []
    lead = {
        "On Track": f"Progress on “{g}” is on track against the “{target}” target.",
        "Early Stage": f"Work on “{g}” is at an early stage under the “{target}” target.",
        "At Risk": f"Delivery of “{g}” is currently at risk and needs attention.",
        "Advanced": f"“{g}” is well advanced under the “{target}” target.",
        "Complete": f"“{g}” has been delivered against the “{target}” target.",
    }
    bits.append(lead.get(status, f"Tracking continues on “{g}”."))
    if primary_name and primary_latest:
        bits.append(
            f"Latest reading on the primary metric ({primary_name}) is {primary_latest} as of {LATEST}."
        )
    tail = rng.choice([
        "Data is refreshed quarterly as reporting from lead ministries lands.",
        "Mock values shown for demonstration; replace with reported figures when available.",
        "Cross-ministry coordination is the main lever for the next reporting period.",
        "Baselines are being confirmed with the accountable teams.",
    ])
    bits.append(tail)
    return " ".join(bits)


def main():
    with open(SRC, encoding="utf-8-sig", newline="") as f:
        goals = list(csv.DictReader(f))

    out_rows = []
    for gi, g in enumerate(goals):
        gid = (g.get("Goal ID") or "").strip()
        if not gid:
            continue
        rng = random.Random(1000 + gi)  # deterministic per goal
        target = (g.get("Target") or "").strip()
        goal_text = (g.get("Goal") or "").strip()

        metrics = [
            (1, g.get("Primary Metric"), g.get("Metric 1 Availability"), g.get("Metric 1 source")),
            (2, g.get("Metric 2"), g.get("Metric 2 Availability"), g.get("Metric 2 source")),
            (3, g.get("Metric 3"), g.get("Metric 3 Availability"), g.get("Metric 3 source")),
        ]

        primary_name = (g.get("Primary Metric") or "").strip()
        primary_latest = ""

        for num, name, avail, source in metrics:
            name = (name or "").strip()
            source = (source or "").strip()
            # The primary metric (#1) always carries a headline value; secondary
            # metrics (#2, #3) appear only when their availability indicates data.
            if not name:
                continue
            if num != 1 and not has_data(avail):
                continue
            kind = metric_kind(name)
            series = gen_series(kind, rng)
            periods = PERIODS if both_periods(avail) else [LATEST]
            for p in periods:
                val, unit = series[p]
                if num == 1 and p == LATEST:
                    primary_latest = _display(val, unit)
                out_rows.append({
                    "Goal ID": gid,
                    "Metric #": str(num),
                    "Metric Name": name,
                    "Metric Value": val,
                    "Unit": unit,
                    "Period": p,
                    "Status": "",
                    "Narrative": "",
                    "Source": source,
                })

        status = rng.choice(STATUSES)
        narrative = make_narrative(goal_text, target, status, primary_name, primary_latest, rng)
        out_rows.append({
            "Goal ID": gid,
            "Metric #": "Summary",
            "Metric Name": "",
            "Metric Value": "",
            "Unit": "",
            "Period": LATEST,
            "Status": status,
            "Narrative": narrative,
            "Source": "",
        })

    with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HEADERS)
        w.writeheader()
        w.writerows(out_rows)

    n_metric = sum(1 for r in out_rows if r["Metric #"] != "Summary")
    n_summary = sum(1 for r in out_rows if r["Metric #"] == "Summary")
    print(f"Wrote {OUT}: {len(out_rows)} rows ({n_metric} metric, {n_summary} summary) for {n_summary} goals.")


def _display(val, unit):
    if unit == "Y/N":
        return val
    if unit == "%":
        return f"{val}%"
    if unit == "$M":
        return f"${val}M"
    if unit == "days":
        return f"{val} days"
    return val


if __name__ == "__main__":
    main()
