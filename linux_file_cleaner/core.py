import os
import shutil
from pathlib import Path
from typing import Iterable, List, Tuple

SizeItem = Tuple[str, int]


def bytes_to_human(size: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(value)} {unit}"
            return f"{value:.2f} {unit}"
        value /= 1024
    return f"{size} B"


def disk_usage(path: str = ".") -> dict:
    total, used, free = shutil.disk_usage(path)
    return {
        "total": total,
        "used": used,
        "free": free,
        "total_human": bytes_to_human(total),
        "used_human": bytes_to_human(used),
        "free_human": bytes_to_human(free),
    }


def safe_walk(folder: str) -> Iterable[Path]:
    root = Path(folder).expanduser()
    if not root.exists():
        return []
    for current, dirs, files in os.walk(root, topdown=True):
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        for name in files:
            path = Path(current) / name
            try:
                if path.is_file() and not path.is_symlink():
                    yield path
            except OSError:
                continue


def find_large_files(folder: str, limit: int = 20) -> List[SizeItem]:
    result: List[SizeItem] = []
    for path in safe_walk(folder):
        try:
            result.append((str(path), path.stat().st_size))
        except OSError:
            continue
    result.sort(key=lambda item: item[1], reverse=True)
    return result[:limit]


def calculate_folder_size(folder: str) -> int:
    total = 0
    for path in safe_walk(folder):
        try:
            total += path.stat().st_size
        except OSError:
            continue
    return total


def find_empty_folders(folder: str, limit: int = 50) -> List[str]:
    root = Path(folder).expanduser()
    result: List[str] = []
    if not root.exists():
        return result
    for current, dirs, files in os.walk(root, topdown=False):
        try:
            if not dirs and not files:
                result.append(current)
        except OSError:
            continue
        if len(result) >= limit:
            break
    return result


def cleanup_preview() -> List[SizeItem]:
    candidates = [
        str(Path.home() / ".cache"),
        "/tmp",
    ]
    result: List[SizeItem] = []
    for folder in candidates:
        path = Path(folder)
        if path.exists():
            result.append((folder, calculate_folder_size(folder)))
    return result
