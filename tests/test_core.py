from pathlib import Path

from linux_file_cleaner.core import bytes_to_human, calculate_folder_size, find_empty_folders, find_large_files


def test_bytes_to_human():
    assert bytes_to_human(100) == "100 B"
    assert bytes_to_human(1024) == "1.00 KB"


def test_calculate_folder_size(tmp_path):
    file_path = tmp_path / "data.txt"
    file_path.write_bytes(b"a" * 10)
    assert calculate_folder_size(str(tmp_path)) == 10


def test_find_large_files(tmp_path):
    small = tmp_path / "small.txt"
    big = tmp_path / "big.txt"
    small.write_bytes(b"a")
    big.write_bytes(b"b" * 100)
    files = find_large_files(str(tmp_path), limit=2)
    assert Path(files[0][0]).name == "big.txt"


def test_find_empty_folders(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    folders = find_empty_folders(str(tmp_path))
    assert str(empty) in folders
