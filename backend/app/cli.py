"""Command-line entry point for reproducible local DepoIndex runs."""
from __future__ import annotations

import argparse
import json

from .services.pipeline import DepoIndexPipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="DepoIndex deposition pipeline")
    parser.add_argument("command", choices=("parse", "run"), help="parse the supplied PDF or generate a complete index run")
    args = parser.parse_args()
    pipeline = DepoIndexPipeline()
    result = pipeline.parse_source() if args.command == "parse" else pipeline.run()
    print(json.dumps(result.get("run", result), indent=2))


if __name__ == "__main__":
    main()
