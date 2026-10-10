from app.export.base import BaseExporter
from app.export.docs_generate import DocsExporter
from app.export.excel_generate import ExcelExporter

_REGISTRY: dict[str, type[BaseExporter]] = {
    "xlsx": ExcelExporter,
    "docx": DocsExporter,
}


def get_exporter(fmt: str) -> BaseExporter:
    return _REGISTRY[fmt.lower()]()


__all__ = ["BaseExporter", "ExcelExporter", "DocsExporter", "get_exporter"]
