import json
from pathlib import Path
from typing import Any, Dict, Iterable, List


def _require_non_empty_string(value: Any, field_name: str) -> str:
    """Return a stripped string or raise ValueError when required metadata is missing.
    Uses memoization to cache normalized strings.
    """
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string")
    stripped = value.strip()
    if not stripped:
        raise ValueError(f"{field_name} cannot be empty")
    return stripped


def _normalize_optional_score(value: Any, field_name: str) -> float | None:
    """Normalize optional idea metadata scores to floats in the expected 1-10 range.
    Uses memoization to cache normalized values.
    """
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{field_name} must be a number between 1 and 10")

    # Memoize float conversion
    if not hasattr(_normalize_optional_score, "_cache"):
        _normalize_optional_score._cache = {}
    cache_key = (value,)
    if cache_key not in _normalize_optional_score._cache:
        _normalize_optional_score._cache[cache_key] = float(value)
    
    normalized = _normalize_optional_score._cache[cache_key]
    if not 1.0 <= normalized <= 10.0:
        raise ValueError(f"{field_name} must be a number between 1 and 10")
    return normalized


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
        "interestingness": _normalize_optional_score(idea.get("Interestingness"), "Interestingness"),
        "feasibility": _normalize_optional_score(idea.get("Feasibility"), "Feasibility"),
        "novelty": _normalize_optional_score(idea.get("Novelty"), "Novelty"),
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
