import csv
import sys
from pathlib import Path


def extract_words(path):
    """Extract word intervals from a Buckeye .words file."""
    rows = []
    last_time = None

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line == "" or line.startswith("signal ") or line.startswith("type ") or line.startswith("comment ") or line.startswith("color ") or line.startswith("font ") or line.startswith("separator ") or line.startswith("nfields ") or line == "#":
                continue

            parts = line.split()
            end = float(parts[0])
            label = parts[2].strip(";").lower()

            if last_time is None:
                last_time = end
                continue

            rows.append((label, last_time, end))
            last_time = end

    return rows


def main():
    """Run the extraction script and save a CSV file."""
    path = sys.argv[1]
    output_path = str(Path(path).with_suffix(".csv"))
    rows = extract_words(path)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["label", "start", "end"])
        for label, start, end in rows:
            writer.writerow([label, start, end])

    print(f"saved {len(rows)} rows to {output_path}")


if __name__ == "__main__":
    main()
