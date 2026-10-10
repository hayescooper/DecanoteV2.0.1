from pathlib import Path

from docx import Document

from app.export.base import BaseExporter


class DocsExporter(BaseExporter):
    extension = "docx"

    def export(self, data: list[dict], out_dir: Path) -> Path:
        doc = Document()
        doc.add_heading("Báo cáo audit - Decanote", level=0)

        for row in data:
            files = row.get("files", [])
            doc.add_heading(f"Nhóm {row.get('chunk')} ({len(files)} file)", level=1)
            for name in files:
                doc.add_paragraph(name, style="List Bullet")
            doc.add_paragraph(row.get("report", ""))

        path = self._make_path(out_dir)
        doc.save(path)
        return path
