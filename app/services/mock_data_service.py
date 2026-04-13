from __future__ import annotations

import json
from pathlib import Path


class MockDataService:
    def __init__(self, config_path: Path | None = None) -> None:
        if config_path is None:
            root = Path(__file__).resolve().parents[2]
            config_path = root / "configs" / "mock_data.json"
        self.config_path = config_path

    def load(self) -> dict:
        with self.config_path.open("r", encoding="utf-8") as file:
            return json.load(file)
