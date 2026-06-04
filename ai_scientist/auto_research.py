import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


def _require_non_empty_string(value: Any, field_name: str) -> str:
    """Return a stripped string or raise ValueError when required metadata is missing."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} is required")
    return value.strip()


def build_hypothesis_record(
    idea: Dict[str, Any],
    success: bool,
    score: float,
    run_path: str,
    timestamp: str,
) -> Dict[str, Any]:
    """Normalize an idea dict into a persisted hypothesis record with minimal validation."""
    return {
        "name": _require_non_empty_string(idea.get("Name"), "Name"),
        "title": idea.get("Title"),
        "hypothesis": _require_non_empty_string(idea.get("Experiment"), "Experiment"),
        "novel": bool(idea.get("novel", False)),
        "interestingness": idea.get("Interestingness"),
        "feasibility": idea.get("Feasibility"),
        "novelty": idea.get("Novelty"),
        "score": float(score),
        "success": bool(success),
        "run_path": _require_non_empty_string(run_path, "run_path"),
        "timestamp": timestamp,
    }


def rank_hypotheses(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort records by score descending, then by timestamp ascending, then by name ascending.
    Missing score treated as -inf. Ensures deterministic ordering across runs.
    """
    return sorted(
        records,
        key=lambda r: (
            -r.get("score", float("-inf")),
            r.get("timestamp", ""),
            r.get("name", ""),
        ),
    )


def append_hypothesis_record(jsonl_path: Path, record: Dict[str, Any]) -> None:
    """Append one hypothesis record to a JSONL file, creating parent dirs if needed."""
    path = Path(jsonl_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
