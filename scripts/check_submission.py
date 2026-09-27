"""Check finalization artifacts without fabricating personal evidence."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS = [
    "README.md",
    "docs/adr/0001-provider-interface.md",
    "docs/adr/0002-frontend-runtime-config.md",
    "docs/adr/0003-deploy-by-sha.md",
    "docs/adr/0004-pii-and-data-governance.md",
    "docs/ENGINEERING-NOTES.md",
    "docs/RUNBOOK.md",
    "docs/AI-USAGE.md",
    "docs/TRIAGE.md",
]
EVIDENCE = [
    "cd-green.png", "ghcr-images.png", "rollout.png", "smoke-test.png",
    "hpa-watch.txt", "hpa-scaling-chart.png", "vpa-recommendation.txt",
    "rollback-rollout-undo.png", "rollback-sha-pin.png", "red-pipeline.png",
    "blocked-merge.png", "green-pipeline.png", "branch-protection.png",
    "merge-conflict.png", "merge-conflict-resolved.png", "git-shortlog.txt",
]


def main() -> int:
    missing_docs = [item for item in DOCS if not (ROOT / item).exists()]
    missing_evidence = [item for item in EVIDENCE if not (ROOT / "docs/evidence" / item).exists()]
    if missing_docs or missing_evidence:
        print("SUBMISSION NOT READY")
        if missing_docs:
            print("Missing documentation:", ", ".join(missing_docs))
        if missing_evidence:
            print("Missing real evidence:", ", ".join(missing_evidence))
        return 1
    print("Documentation and evidence files are present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
