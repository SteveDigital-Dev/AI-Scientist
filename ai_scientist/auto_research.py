import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


def build_hypothesis_record(
    idea: Dict[str, Any],
    success: bool,
    score: float,
    run_path: str,
    timestamp: str,
) -> Dict[str, Any]:
    """Normalize an idea dict into a persisted hypothesis record."""
    return {
        "name": idea.get("Name"),
        "title": idea.get("Title"),
        "hypothesis": idea.get("Experiment"),
        "novel": bool(idea.get("novel", False)),
        "interestingness": idea.get("Interestingness"),
        "feasibility": idea.get("Feasibility"),
        "novelty": idea.get("Novelty"),
        "score": float(score),
        "success": bool(success),
        "run_path": run_path,
        "timestamp": timestamp,
    }


def rank_hypotheses(records: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort records by score descending (missing score treated as -inf)."""
    return sorted(records, key=lambda r: r.get("score", float("-inf")), reverse=True)


def append_hypothesis_record(jsonl_path: Path, record: Dict[str, Any]) -> None:
    """Append one hypothesis record to a JSONL file, creating parent dirs if needed."""
    path = Path(jsonl_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
