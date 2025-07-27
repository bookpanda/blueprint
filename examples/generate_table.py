import os
import re


def extract_last_cumulative_time(filepath):
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
            matches = [
                re.search(r"cumulative time ([\d.]+)([a-z]+)", line) for line in lines
            ]
            matches = [(float(m.group(1)), m.group(2)) for m in matches if m]
            return matches[-1] if matches else ("", "")
    except Exception:
        return ("", "")


def convert_to_ms(value, unit):
    if unit == "s":
        return value * 1000
    elif unit == "ms":
        return value
    elif unit == "us":
        return value / 1000
    else:
        return None  # unknown unit


def format_time(ms):
    if ms is None:
        return ""
    return f"{ms:.3f}ms" if ms < 1000 else f"{ms/1000:.3f}s"


def collect_times(base_dir):
    data = {}
    for dirpath, _, filenames in os.walk(base_dir):
        for file in filenames:
            if file.endswith(".log"):
                spec = file.replace(".log", "")
                dir_name = os.path.basename(dirpath)
                key = f"{dir_name} - {spec}"
                full_path = os.path.join(dirpath, file)
                value, unit = extract_last_cumulative_time(full_path)
                ms = convert_to_ms(value, unit) if value != "" else None
                data[key] = ms
    return data


def generate_table(cached_times, no_cached_times):
    keys = sorted(set(cached_times.keys()) | set(no_cached_times.keys()))
    table = "| App + Spec           | no cached | cached   | change   | % change |\n"
    table += "|----------------------|-----------|----------|----------|----------|\n"

    total_no_cached = 0
    total_cached = 0
    percent_changes = []

    for key in keys:
        no_cached_ms = no_cached_times.get(key)
        cached_ms = cached_times.get(key)

        no_cached_str = format_time(no_cached_ms)
        cached_str = format_time(cached_ms)

        if no_cached_ms is not None and cached_ms is not None:
            change_ms = cached_ms - no_cached_ms
            pct_change = (change_ms / no_cached_ms) * 100 if no_cached_ms != 0 else 0
            change_str = f"{change_ms:+.3f}ms"
            pct_str = f"{pct_change:+.2f}%"

            total_no_cached += no_cached_ms
            total_cached += cached_ms
            percent_changes.append(pct_change)
        else:
            change_str = ""
            pct_str = ""

        table += f"| {key:<22} | {no_cached_str:<9} | {cached_str:<8} | {change_str:<8} | {pct_str:<8} |\n"

    # Totals row
    if total_no_cached > 0:
        total_change = total_cached - total_no_cached
        avg_pct_change = total_change / total_no_cached * 100 if total_no_cached else 0

        total_no_cached_str = format_time(total_no_cached)
        total_cached_str = format_time(total_cached)
        total_change_str = f"{total_change:+.3f}ms"
        avg_pct_change_str = f"{avg_pct_change:+.2f}%"

        table += (
            "|----------------------|-----------|----------|----------|----------|\n"
        )
        table += f"| TOTAL                | {total_no_cached_str:<9} | {total_cached_str:<8} | {total_change_str:<8} | {avg_pct_change_str:<8} |\n"

    return table


if __name__ == "__main__":
    cached = collect_times("./results_cached")
    no_cached = collect_times("./results_no_cached")
    print(generate_table(cached, no_cached))
