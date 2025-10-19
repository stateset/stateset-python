from __future__ import annotations

from datetime import datetime
import copy
import io
from pathlib import Path

import pytest

from stateset.types import (
    File,
    FileUploadError,
    PaginatedList,
    PaginationParams,
    StatesetObject,
    UNSET,
)


def test_stateset_object_coerces_timestamp_fields() -> None:
    obj = StatesetObject(
        id="obj_1",
        object="order",
        created=1_672_531_200,
        updated="1672531260",
    )
    assert isinstance(obj.created, datetime)
    assert isinstance(obj.updated, datetime)


def test_file_from_path_prepares_upload(tmp_path: Path) -> None:
    file_path = tmp_path / "document.txt"
    file_path.write_text("hello", encoding="utf-8")

    file = File.from_path(file_path, purpose="warranty_evidence")
    name, stream, mime = file.to_upload_data()
    try:
        assert name == "document.txt"
        assert stream.read() == b"hello"
        assert mime == "text/plain"
    finally:
        stream.close()


def test_file_to_upload_data_from_string_payload() -> None:
    file = File(payload="greeting", file_name="note.txt")
    name, stream, mime = file.to_upload_data()
    try:
        assert name == "note.txt"
        assert stream.read() == b"greeting"
        assert mime is None
    finally:
        stream.close()


def test_file_to_upload_requires_binary_mode(tmp_path: Path) -> None:
    file_path = tmp_path / "plain.txt"
    file_path.write_text("text", encoding="utf-8")

    with file_path.open("r", encoding="utf-8") as handle:
        file = File(payload=handle, file_name="plain.txt")
        with pytest.raises(FileUploadError):
            file.to_upload_data()


def test_file_to_upload_data_rejects_unknown_payload() -> None:
    file = File(payload=object())
    with pytest.raises(FileUploadError):
        file.to_upload_data()


def test_file_from_path_raises_for_missing_file(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.txt"
    with pytest.raises(FileUploadError):
        File.from_path(missing_path)


def test_file_to_upload_data_from_bytes_payload() -> None:
    file = File(payload=b"bytes", file_name="blob.bin", mime_type="application/octet-stream")
    name, stream, mime = file.to_upload_data()
    try:
        assert name == "blob.bin"
        assert stream.read() == b"bytes"
        assert mime == "application/octet-stream"
    finally:
        stream.close()


def test_file_to_upload_data_from_binary_stream() -> None:
    buffer = io.BytesIO(b"data")
    file = File(payload=buffer, file_name="buffer.bin")
    name, stream, mime = file.to_upload_data()
    assert name == "buffer.bin"
    assert stream is buffer
    assert mime is None


def test_unset_behaviour() -> None:
    assert not UNSET
    assert repr(UNSET) == "UNSET"
    assert copy.copy(UNSET) is UNSET
    assert copy.deepcopy(UNSET) is UNSET


def test_pagination_helpers() -> None:
    params = PaginationParams()
    assert params.page == 1

    page = PaginatedList(
        data=[1, 2],
        total=4,
        page=2,
        per_page=2,
        total_pages=2,
        has_next=False,
        has_prev=True,
    )
    assert page.next_page is None
    assert page.prev_page == 1
