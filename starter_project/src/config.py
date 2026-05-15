from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = PROJECT_ROOT.parent


def _load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return

    try:
        from dotenv import load_dotenv
    except ImportError:
        for line in env_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("\"'"))
    else:
        load_dotenv(env_path, override=False)


_load_env_file(REPO_ROOT / ".env")
_load_env_file(PROJECT_ROOT / ".env")

DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"

PASSED_DATASET = DATA_DIR / "orders_passed.csv"
FAILED_DATASET = DATA_DIR / "orders_failed.csv"
SUMMARY_FILE = OUTPUT_DIR / "validation_summary.json"

VALID_STATUSES = {"completed", "pending", "cancelled"}


def _resolve_input_file(raw_path: str) -> str:
    input_path = Path(raw_path).expanduser()
    if input_path.is_absolute():
        return str(input_path)

    project_relative_path = (PROJECT_ROOT / input_path).resolve()
    if project_relative_path.exists():
        return str(project_relative_path)

    repo_relative_path = (REPO_ROOT / input_path).resolve()
    if repo_relative_path.exists():
        return str(repo_relative_path)

    return str(project_relative_path)


DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
AIRFLOW_INPUT_FILE = _resolve_input_file(os.getenv("AIRFLOW_INPUT_FILE", str(PASSED_DATASET)))
