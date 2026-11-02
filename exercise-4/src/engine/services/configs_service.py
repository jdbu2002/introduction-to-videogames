import json
from typing import Any

from src.utils.parse_path import parse_path


class ConfigsService:
    def __init__(self) -> None:
        self._configs: dict[str, Any] = {}

    def get(self, path: str) -> Any:
        if path not in self._configs:
            with open(parse_path(path), encoding="utf-8") as f:
                self._configs[path] = json.load(f)
        return self._configs[path]
