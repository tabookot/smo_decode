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

        lo = ((c1 - ord('A') + 10) ^ 5) & 0x0F
        hi = ((c2 - ord('A') + 10) ^ 5) & 0x0F

        value = lo | (hi << 4)

        if value == 0x5F:
            out.append(ord('\n'))
            continue

        out.append(value)

    return bytes(out)


def is_hex_garbage(line: str) -> bool:
    parts = line.split()
    if len(parts) < 3:
        return False
    return all(p in "0123456789ABCDEF" for p in parts)


def parse_and_build_report(text: str) -> str:
    """
    Парсит лог, извлекает статику, ошибки и собирает
    таблицу параметров по тактам + графики (спарклайны).
    """
    lines = text.splitlines()

    info_lines = []
    dtc_lines = []
    cycles = []

    current_cycle = {}
    in_param_name = False
    param_name_parts = []

    last_param_name = ""
    is_string_val = False
    last_param_value = ""

    # Мусорные шаблоны
    skip_patterns = [
        "Bluetooth State -", "Read block -", "Data block created!",
        "Message Group Sending", "****", "Abstract Activity",
        "Create Tabs", "Create -", "Android OS", "Device Name", "Device Model",
        "Package name", "App Version", "BUS INIT",
        "Repeat Data Reading", "Owner Changed", "Live Data Off", "Live Data On",
        "Adapter Test", "Adapter Init", "ECU Init", "Selector Init", "TC Read"
    ]

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if is_hex_garbage(line):
            continue

        if any(skip in line for skip in skip_patterns):
            # Фиксируем момент стирания ошибок
            if "Data array Length is 0" in line and dtc_lines:
                dtc_lines.append("--- Ошибки стерты (Trouble Codes Cleared) ---")
            continue

        if line.startswith("AT") or line in (">", ">>"):
            continue

        # 1. Статика об ЭБУ
        if "Name:" in line and "Value:" in line:
            info_lines.append(line.split(" - ", 1)[-1])
            continue

        # 2. Коды ошибок
        if "Code:" in line and "Name:" in line:
            err = line.split(" - ", 1)[-1]
            if err not in dtc_lines:
                dtc_lines.append(err)
            continue

        # 3. Live Data (Сборка циклов)
        if "Parameter Name -" in line:
            # Если до этого был параметр, сохраняем его в текущий цикл
            if last_param_name:
                current_cycle[last_param_name] = last_param_value

            in_param_name = True
            param_name_parts = []
            last_param_value = ""
            is_string_val = False
            last_param_name = ""
            continue

        if in_param_name:
            if "Parameter Formula" in line:
                in_param_name = False
                last_param_name = " ".join(param_name_parts).strip()
            else:
                clean_part = line.split(" - ", 1)[-1] if " - " in line else line
                param_name_parts.append(clean_part)
            continue

        if "Value S -" in line:
            val = line.split("Value S -", 1)[-1].strip()
            if val != "null":
                last_param_value = val
                is_string_val = True
            continue

        if "Value D -" in line:
            if not is_string_val:
                last_param_value = line.split("Value D -", 1)[-1].strip()
            continue

        # Конец цикла опроса (начинается новый запрос данных)
        if "Update adapter info" in line:
            if last_param_name:
                current_cycle[last_param_name] = last_param_value
                last_param_name = ""

            if current_cycle:
                cycles.append(current_cycle)
                current_cycle = {}
            continue

    # Захватываем последний параметр и цикл
    if last_param_name:
        current_cycle[last_param_name] = last_param_value
    if current_cycle:
        cycles.append(current_cycle)

    # --- ФОРМИРОВАНИЕ ОТЧЕТА ---
    report = []

    report.append("=== ИНФОРМАЦИЯ ОБ ЭБУ ===")
    report.extend(info_lines)
    report.append("\n=== КОДЫ ОШИБОК (DTC) ===")
    if dtc_lines:
        report.extend(dtc_lines)
    else:
        report.append("Ошибок не найдено.")

    report.append(f"\n=== ЖИВЫЕ ДАННЫЕ (LIVE DATA) ===")
    report.append(f"Всего зафиксировано тактов опроса: {len(cycles)}\n")

    if not cycles:
        report.append("Данные Live Data не обнаружены.")
        return "\n".join(report)

    # Собираем все уникальные имена параметров
    all_params = []
    for cycle in cycles:
        for p in cycle.keys():
            if p not in all_params:
                all_params.append(p)

    # --- ТАБЛИЦА (Параметры по строкам, такты по колонкам) ---
    report.append("=== ТАБЛИЦА ЗНАЧЕНИЙ ПО ТАКТАМ ===")
    # Шапка таблицы
    header = f"{'Параметр':<35} | " + " | ".join([f"T{i:<3}" for i in range(len(cycles))])
    report.append(header)
    report.append("-" * len(header))

    for p in all_params:
        row_vals = []
        for cycle in cycles:
            val = cycle.get(p, "-")
            # Обрезаем слишком длинные значения для таблицы
            val_str = str(val)[:5]
            row_vals.append(f"{val_str:<4}")

        p_name = (p[:33] + '..') if len(p) > 33 else p
        report.append(f"{p_name:<35} | " + " | ".join(row_vals))

    # --- ДИАГРАММЫ (Спарклайны для цифровых данных) ---
    report.append("\n=== ГРАФИКИ ИЗМЕНЕНИЙ ===")
    spark_chars = "▁▂▃▄▅▆▇█"

    for p in all_params:
        values = []
        is_numeric = True

        for cycle in cycles:
            val = cycle.get(p)
            if val is None or val == "-":
                values.append(None)
            else:
                try:
                    values.append(float(val))
                except ValueError:
                    is_numeric = False
                    break

        if not is_numeric:
            continue

        valid_vals = [v for v in values if v is not None]
        if not valid_vals:
            continue

        min_v, max_v = min(valid_vals), max(valid_vals)
        range_v = max_v - min_v

        sparkline = ""
        for v in values:
            if v is None:
                sparkline += " "
            elif range_v == 0:
                sparkline += spark_chars[4] # средний уровень
            else:
                norm = (v - min_v) / range_v
                idx = int(norm * 7)
                idx = max(0, min(7, idx))
                sparkline += spark_chars[idx]

        # Красивое форматирование Min/Max
        min_str = f"{min_v:.2f}".rstrip('0').rstrip('.')
        max_str = f"{max_v:.2f}".rstrip('0').rstrip('.')

        report.append(f"{p}")
        report.append(f"  Min: {min_str:<8} Max: {max_str:<8} | {sparkline}")
        report.append("")

    return "\n".join(report)


def convert_file(path: Path):
    with open(path, "rb") as f:
        encoded = f.read()

    decoded = decode_smo(encoded)

    try:
        text = decoded.decode("utf-8")
    except UnicodeDecodeError:
        text = decoded.decode("utf-8", errors="replace")

    # Генерация таблиц и графиков
    report_text = parse_and_build_report(text)

    output_path = path.with_suffix(".txt")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_text)

    print(f"Готово. Файл обработан: {path.name}")
    print(f"Результат сохранен в: {output_path.name}")


def main():
    if len(sys.argv) == 2:
        path = Path(sys.argv[1])
        if not path.exists():
            print("Файл не найден:", path)
            return
        convert_file(path)
        return

    current_dir = Path.cwd()
    files = sorted(current_dir.glob("*.smo"))

    if not files:
        print(f"В папке '{current_dir}' файлы .smo не найдены.")
        return

    print(f"Найдено файлов: {len(files)}\n")

    for file in files:
        try:
            convert_file(file)
        except Exception as e:
            print(f"\nОшибка при обработке '{file}':")
            print(e)

if __name__ == "__main__":
    main()