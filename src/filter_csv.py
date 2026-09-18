import csv
import sys
from pathlib import Path


def filter_rows(path):
    """Filter out non-word labels such as <SIL> and <NOISE>."""
    rows = []

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            label = row["label"].strip().lower()

            # Skip tags written inside angle brackets.
            if label.startswith("<") and label.endswith(">"):
                continue

            # Skip tags written inside curly braces.
            if label.startswith("{") and label.endswith("}"):
                continue

            rows.append((label, row["start"], row["end"]))

    return rows


def main():
    """Run the filtering script and save a cleaned CSV file."""
    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else str(Path(input_path).with_stem(Path(input_path).stem + "_filtered"))
    rows = filter_rows(input_path)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["label", "start", "end"])
        for label, start, end in rows:
            writer.writerow([label, start, end])

    print(f"saved {len(rows)} rows to {output_path}")


if __name__ == "__main__":
    main()
