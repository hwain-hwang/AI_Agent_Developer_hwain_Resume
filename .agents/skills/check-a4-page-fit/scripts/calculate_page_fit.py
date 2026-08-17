#!/usr/bin/env python3
"""Calculate A4 printable-area utilization from a measured content height."""

from __future__ import annotations

import argparse
import json


MM_PER_CSS_PX = 25.4 / 96


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate A4 page utilization and remaining printable height."
    )
    parser.add_argument("--used", type=float, required=True, help="Current content height.")
    parser.add_argument(
        "--delta",
        type=float,
        default=0,
        help="Net height change: additions and gaps minus removed height.",
    )
    parser.add_argument("--unit", choices=("mm", "px"), default="mm")
    parser.add_argument("--page-height", type=float, default=297)
    parser.add_argument("--top-margin", type=float, default=11)
    parser.add_argument("--bottom-margin", type=float, default=11)
    parser.add_argument("--safe-limit", type=float, default=95)
    return parser.parse_args()


def to_mm(value: float, unit: str) -> float:
    return value if unit == "mm" else value * MM_PER_CSS_PX


def main() -> None:
    args = parse_args()
    printable_mm = args.page_height - args.top_margin - args.bottom_margin
    if printable_mm <= 0:
        raise SystemExit("Printable height must be greater than zero.")
    if not 0 < args.safe_limit <= 100:
        raise SystemExit("Safe limit must be greater than 0 and at most 100.")

    used_mm = to_mm(args.used, args.unit)
    delta_mm = to_mm(args.delta, args.unit)
    projected_mm = used_mm + delta_mm
    usage_percent = projected_mm / printable_mm * 100
    remaining_mm = printable_mm - projected_mm

    if usage_percent > 100:
        status = "OVERFLOW"
    elif usage_percent > args.safe_limit:
        status = "TIGHT"
    else:
        status = "SAFE"

    result = {
        "printable_height_mm": round(printable_mm, 2),
        "used_height_mm": round(used_mm, 2),
        "delta_mm": round(delta_mm, 2),
        "projected_height_mm": round(projected_mm, 2),
        "usage_percent": round(usage_percent, 2),
        "remaining_mm": round(remaining_mm, 2),
        "status": status,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
