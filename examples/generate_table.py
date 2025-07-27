import os
import re

def extract_cumulative_time(filepath):
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
            if not lines:
                return ""
            last_line = lines[-1].strip()
            match = re.search(r"cumulative time ([\d.]+s)", last_line)
            return match.group(1) if match else ""
    except Exception as e:
        return ""

def collect_times(base_dir):
    data = {}
    for dirpath, _, filenames in os.walk(base_dir):
        for file in filenames:
            if file.endswith(".log"):
                spec = file.replace(".log", "")
                dir_name = os.path.basename(dirpath)
                key = f"{dir_name} - {spec}"
                full_path = os.path.join(dirpath, file)
                time = extract_cumulative_time(full_path)
                data[key] = time
    return data

def generate_table(cached_times, no_cached_times):
    keys = sorted(set(cached_times.keys()) | set(no_cached_times.keys()))
    table = "| Directory + Spec | no cached | cached |\n"
    table += "|------------------|-----------|--------|\n"
    for key in keys:
        no_cached = no_cached_times.get(key, "")
        cached = cached_times.get(key, "")
        table += f"| {key:<16} | {no_cached:<9} | {cached:<6} |\n"
    return table

if __name__ == "__main__":
    cached_times = collect_times("./results_cached")
    no_cached_times = collect_times("./results_no_cached")
    markdown_table = generate_table(cached_times, no_cached_times)
    print(markdown_table)
