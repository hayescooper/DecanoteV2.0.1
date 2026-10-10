"""Gom file thành từng nhóm (mặc định 20 file) để gửi AI audit.

Thuần Python, không phụ thuộc web/AI nên dễ test.
"""
from __future__ import annotations

from typing import Iterable, Iterator, Sequence, TypeVar

from app.core.utils.file_processor import extract_text_from_file

T = TypeVar("T")

DEFAULT_CHUNK_SIZE = 20


def chunk_list(items: Sequence[T], size: int = DEFAULT_CHUNK_SIZE) -> list[list[T]]:
    """Chia danh sách thành các nhóm tối đa `size` phần tử."""
    if size <= 0:
        raise ValueError("size phải > 0")
    return [list(items[i : i + size]) for i in range(0, len(items), size)]


def iter_chunks(items: Iterable[T], size: int = DEFAULT_CHUNK_SIZE) -> Iterator[list[T]]:
    """Phiên bản generator: không cần nạp hết 1000 file vào RAM trước."""
    if size <= 0:
        raise ValueError("size phải > 0")
    batch: list[T] = []
    for item in items:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


def build_prompt(chunk: Sequence[dict], instruction: str) -> str:
    """Ghép hướng dẫn + nội dung từng file thành 1 prompt cho AI."""
    parts = [instruction.strip(), ""]
    for i, item in enumerate(chunk, start=1):
        parts.append(f"----- FILE {i}: {item['name']} -----")
        parts.append(item["content"])
        parts.append("")
    return "\n".join(parts)

def prepare_files_for_ai(file_list):
    processed_data = []
    for f_path in file_list:
        content = extract_text_from_file(f_path)
        processed_data.append({"name": f_path, "content": content})
    return processed_data
