"""Interface chung cho mọi exporter: export(data) -> file."""
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path


class BaseExporter(ABC):
    extension: str = ""

    @abstractmethod
    def export(self, data: list[dict], out_dir: Path) -> Path:
        """data: [{"chunk": int, "files": [str], "report": str}, ...]"""

    def _make_path(self, out_dir: Path) -> Path:
        out_dir = Path(out_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return out_dir / f"decanote_{stamp}.{self.extension}"
