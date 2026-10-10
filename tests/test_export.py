from app.export import get_exporter

SAMPLE = [{"chunk": 1, "files": ["a.py", "b.py"], "report": "Không có lỗi."}]


def test_export_excel(tmp_path):
    path = get_exporter("xlsx").export(SAMPLE, tmp_path)
    assert path.exists() and path.suffix == ".xlsx"


def test_export_docx(tmp_path):
    path = get_exporter("docx").export(SAMPLE, tmp_path)
    assert path.exists() and path.suffix == ".docx"
