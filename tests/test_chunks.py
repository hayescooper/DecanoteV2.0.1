import pytest

from app.core.scan.chunks import build_prompt, chunk_list, filter_ignored_files, iter_chunks


def test_chunk_list_1000_files_thanh_50_nhom():
    chunks = chunk_list(list(range(1000)), 20)
    assert len(chunks) == 50
    assert all(len(c) == 20 for c in chunks)


def test_nhom_cuoi_con_du():
    chunks = chunk_list(list(range(45)), 20)
    assert [len(c) for c in chunks] == [20, 20, 5]


def test_iter_chunks_giong_chunk_list():
    assert list(iter_chunks(range(45), 20)) == chunk_list(list(range(45)), 20)


def test_size_khong_hop_le():
    with pytest.raises(ValueError):
        chunk_list([1], 0)
    with pytest.raises(ValueError):
        list(iter_chunks([1], -1))


def test_build_prompt_chua_ten_file():
    prompt = build_prompt([{"name": "a.py", "content": "print(1)"}], "Audit")
    assert "a.py" in prompt and "print(1)" in prompt


