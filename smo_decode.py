#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple ScanMyOpel *.smo log decoder.

Decodes proprietary .smo files into plain UTF-8 text without additional
filtering or visualization.
"""

from pathlib import Path
import sys
from typing import Dict, List, Optional

__version__ = "0.1.4"  # Build counter: increment last digit on every release

# -----------------------------------------------------------------------------
# Localization
# -----------------------------------------------------------------------------
_MESSAGES: Dict[str, Dict[str, str]] = {
    "en": {
        "warning_odd_length": "Warning: odd file length.",
        "file_not_found": "File not found:",
        "no_smo_files": "No .smo files found in directory '{}'.",
        "files_found": "Files found: {}",
        "done": "Done.",
        "source_file": "Source file:",
        "result_file": "Result file:",
        "processed_ok": "Successfully processed: {}",
        "errors": "Errors: {}",
        "error_processing": "Error processing '{}':",
        "file_too_large": "File is too large: {:.1f} MB (max {:.1f} MB)",
        "write_error": "Failed to write output file",
        "invalid_path": "Invalid file path: {}",
    },
    "ru": {
        "warning_odd_length": "Предупреждение: нечётная длина файла.",
        "file_not_found": "Файл не найден:",
        "no_smo_files": "В папке '{}' файлы .smo не найдены.",
        "files_found": "Найдено файлов: {}",
        "done": "Готово.",
        "source_file": "Исходный файл:",
        "result_file": "Результат:",
        "processed_ok": "Успешно обработано: {}",
        "errors": "Ошибок: {}",
        "error_processing": "Ошибка при обработке '{}':",
        "file_too_large": "Файл слишком большой: {:.1f} МБ (макс. {:.1f} МБ)",
        "write_error": "Не удалось записать выходной файл",
        "invalid_path": "Некорректный путь к файлу: {}",
    },
}


def _get_messages(lang: str = "en") -> Dict[str, str]:
    """Return localized message dictionary."""
    return _MESSAGES.get(lang, _MESSAGES["en"])


# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------
MAX_FILE_SIZE: int = 50 * 1024 * 1024  # 50 MB safety limit


# -----------------------------------------------------------------------------
# Core decoder
# -----------------------------------------------------------------------------


def decode_smo(data: bytes) -> bytes:
    """Decode ScanMyOpel *.smo file content.

    The encoding scheme maps each byte to two ASCII characters (A-P range),
    applies XOR 0x05 and nibble swap. Newline marker is 0x5F ('KF').

    Args:
        data: Raw encoded bytes from .smo file.

    Returns:
        Decoded bytearray as bytes.
    """
    out = bytearray()

    if len(data) % 2 != 0:
        print(_get_messages()["warning_odd_length"])

    for i in range(0, len(data) - 1, 2):
        c1 = data[i]
        c2 = data[i + 1]

        # Original encoding logic preserved (see rev. point #13)
        lo = ((c1 - ord("A") + 10) ^ 5) & 0x0F
        hi = ((c2 - ord("A") + 10) ^ 5) & 0x0F

        value = lo | (hi << 4)

        if value == 0x5F:
            out.append(ord("\n"))
            continue

        out.append(value)

    return bytes(out)


# -----------------------------------------------------------------------------
# Input validation and I/O helpers
# -----------------------------------------------------------------------------


def validate_path(path: Path) -> Path:
    """Validate that the path does not escape the working directory.

    Args:
        path: Input file path.

    Returns:
        Resolved absolute path.

    Raises:
        ValueError: If path points outside the current working directory.
    """
    resolved = path.resolve()
    cwd = Path.cwd().resolve()
    try:
        resolved.relative_to(cwd)
    except ValueError as exc:
        raise ValueError(_get_messages()["invalid_path"].format(path)) from exc
    return resolved


def check_file_size(path: Path, max_size: int = MAX_FILE_SIZE) -> None:
    """Check that the file size is within the allowed limit.

    Args:
        path: File to check.
        max_size: Maximum allowed size in bytes.

    Raises:
        ValueError: If the file exceeds max_size.
    """
    size = path.stat().st_size
    if size > max_size:
        raise ValueError(
            _get_messages()["file_too_large"].format(
                size / 1024 / 1024, max_size / 1024 / 1024
            )
        )


def safe_write(path: Path, content: str, messages: Dict[str, str]) -> None:
    """Write text to file with error handling.

    Args:
        path: Output file path.
        content: Text content to write.
        messages: Localized message dictionary for error strings.

    Raises:
        OSError: If writing fails after logging the error.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    except OSError as exc:
        print(f"{messages['write_error']}: {path} — {exc}")
        raise


# -----------------------------------------------------------------------------
# File conversion
# -----------------------------------------------------------------------------


def convert_file(path: Path, lang: str = "en") -> None:
    """Convert a single .smo file to decoded .txt.

    Args:
        path: Path to the .smo file.
        lang: Language code ('en' or 'ru').
    """
    messages = _get_messages(lang)

    validated = validate_path(path)
    check_file_size(validated)

    with open(validated, "rb") as f:
        encoded = f.read()

    decoded = decode_smo(encoded)

    try:
        text = decoded.decode("utf-8")
    except UnicodeDecodeError:
        text = decoded.decode("utf-8", errors="replace")

    output_path = path.with_suffix(".txt")
    safe_write(output_path, text, messages)

    print(f"{messages['done']}")
    print(f"{messages['source_file']} {path}")
    print(f"{messages['result_file']} {output_path}")


# -----------------------------------------------------------------------------
# CLI entry point
# -----------------------------------------------------------------------------


def main(argv: Optional[List[str]] = None) -> None:
    """Command-line entry point.

    Args:
        argv: Optional argument list override (for testing).
    """
    if argv is None:
        argv = sys.argv[1:]

    lang = "en"
    args = list(argv)

    if "--lang" in args:
        idx = args.index("--lang")
        if idx + 1 < len(args):
            lang = args[idx + 1]
            args.pop(idx)
            args.pop(idx)
    elif "-l" in args:
        idx = args.index("-l")
        if idx + 1 < len(args):
            lang = args[idx + 1]
            args.pop(idx)
            args.pop(idx)

    if args:
        path = Path(args[0])
        if not path.exists():
            print(f"{_get_messages(lang)['file_not_found']} {path}")
            return
        convert_file(path, lang)
        return

    current_dir = Path.cwd()
    files = sorted(current_dir.glob("*.smo"))

    if not files:
        print(_get_messages(lang)["no_smo_files"].format(current_dir))
        return

    print(f"{_get_messages(lang)['files_found'].format(len(files))}\n")

    ok = 0
    bad = 0

    for file in files:
        try:
            convert_file(file, lang)
            ok += 1
        except Exception as exc:
            bad += 1
            print(f"\n{_get_messages(lang)['error_processing'].format(file)}")
            print(exc)

    messages = _get_messages(lang)
    print(f"\n{messages['done']}")
    print(f"{messages['processed_ok'].format(ok)}")
    print(f"{messages['errors'].format(bad)}")


if __name__ == "__main__":
    main()
