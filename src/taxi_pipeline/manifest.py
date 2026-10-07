from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class ManifestEntry:
    dataset: str
    year: int
    month: int
    source_file: str
    status: str
    rows_loaded: int


class Manifest:
    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.entries = self._read()

    def _read(self) -> list[dict]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def is_complete(self, dataset: str, year: int, month: int) -> bool:
        return any(
            entry["dataset"] == dataset
            and entry["year"] == year
            and entry["month"] == month
            and entry["status"] == "complete"
            for entry in self.entries
        )

    def upsert(self, entry: ManifestEntry) -> None:
        self.entries = [
            item
            for item in self.entries
            if not (
                item["dataset"] == entry.dataset
                and item["year"] == entry.year
                and item["month"] == entry.month
            )
        ]
        self.entries.append(asdict(entry))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.entries, indent=2), encoding="utf-8")
