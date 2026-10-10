"""Chỉ định tuyến: nhận request, gọi core/export, trả response."""
from pathlib import Path

from flask import Blueprint, current_app, jsonify, request, send_file

from app.core.clients.gemini import audit
from app.core.scan.chunks import build_prompt, iter_chunks
from app.export import get_exporter

bp = Blueprint("scan", __name__)


def _read_uploads(rules: dict) -> list[dict]:
    allowed = {e.lower() for e in rules["allowed_extensions"]}
    limit = rules["max_file_bytes"]
    items = []
    for f in request.files.getlist("files"):
        name = f.filename or "unnamed"
        if Path(name).suffix.lower() not in allowed:
            continue
        raw = f.read(limit)
        items.append({"name": name, "content": raw.decode("utf-8", errors="replace")})
    return items


@bp.post("/api/scan")
def scan():
    rules = current_app.config["RULES"]
    items = _read_uploads(rules)
    if not items:
        return jsonify(error="Không có file hợp lệ."), 400

    results = []
    for idx, chunk in enumerate(iter_chunks(items, rules["chunk_size"]), start=1):
        prompt = build_prompt(chunk, rules["audit_prompt"])
        try:
            report = audit(prompt)
        except Exception as exc:  # lỗi 1 nhóm không làm hỏng cả lượt
            report = f"[LỖI] {exc}"
        results.append({"chunk": idx, "files": [i["name"] for i in chunk], "report": report})

    return jsonify(total_files=len(items), results=results)


@bp.post("/api/export")
def export():
    payload = request.get_json(silent=True) or {}
    fmt = payload.get("format", "xlsx")
    results = payload.get("results", [])
    try:
        exporter = get_exporter(fmt)
    except KeyError:
        return jsonify(error=f"Định dạng không hỗ trợ: {fmt}"), 400

    out_dir = Path(current_app.config["EXPORT_DIR"])
    path = exporter.export(results, out_dir)
    return send_file(path, as_attachment=True, download_name=path.name)
