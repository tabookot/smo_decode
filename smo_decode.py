#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import sys


def decode_smo(data: bytes) -> bytes:
    """
    Декодирует содержимое файла ScanMyOpel (*.smo).
    """

    out = bytearray()

    if len(data) % 2 != 0:
        print("Предупреждение: нечётная длина файла.")

    for i in range(0, len(data) - 1, 2):
        c1 = data[i]
        c2 = data[i + 1]

        # преобразование символов обратно в полубайты
        lo = ((c1 - ord('A') + 10) ^ 5) & 0x0F
        hi = ((c2 - ord('A') + 10) ^ 5) & 0x0F

        value = lo | (hi << 4)

        # маркер конца записи ("KF")
        if value == 0x5F:
            out.append(ord('\n'))
            continue

        out.append(value)

    return bytes(out)


def convert_file(path: Path):

    with open(path, "rb") as f:
        encoded = f.read()

    decoded = decode_smo(encoded)

    output_path = path.with_suffix(".txt")

    try:
        text = decoded.decode("utf-8")
    except UnicodeDecodeError:
        text = decoded.decode("utf-8", errors="replace")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print(f"Готово.")
    print(f"Исходный файл: {path}")
    print(f"Результат:     {output_path}")


def main():

    # Указан конкретный файл
    if len(sys.argv) == 2:

        path = Path(sys.argv[1])

        if not path.exists():
            print("Файл не найден:", path)
            return

        convert_file(path)
        return

    # Аргументов нет — ищем все .smo рядом со скриптом
    current_dir = Path.cwd()

    files = sorted(current_dir.glob("*.smo"))

    if not files:
        print(f"В папке '{current_dir}' файлы .smo не найдены.")
        return

    print(f"Найдено файлов: {len(files)}\n")

    ok = 0
    bad = 0

    for file in files:

        try:
            convert_file(file)
            ok += 1

        except Exception as e:
            bad += 1
            print(f"\nОшибка при обработке '{file}':")
            print(e)

    print("\nГотово.")
    print(f"Успешно обработано: {ok}")
    print(f"Ошибок: {bad}")

if __name__ == "__main__":
    main()