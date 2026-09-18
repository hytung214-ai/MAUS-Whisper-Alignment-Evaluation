import csv
import sys
from pathlib import Path


def extract_intervals(path, tier_name):
    """Extract word intervals from the selected TextGrid tier."""
    # Store each extracted word interval as (start, end, text).
    rows = []

    # These flags keep track of whether we are currently inside
    # the tier we want and inside one specific interval block.
    inside_tier = False
    inside_interval = False

    # Temporary variables for one interval.
    start = None
    end = None
    text = None

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

            if line.startswith("item ["):
                # A new item means we leave the previous tier/interval.
                inside_tier = False
                inside_interval = False
                start, end, text = None, None, None
                continue

            if line.startswith("name ="):
                # Only read the tier we need for this assignment.
                name = line.split("=", 1)[1].strip().strip('"')
                inside_tier = name == tier_name
                inside_interval = False
                start, end, text = None, None, None
                continue

            if not inside_tier:
                # Skip everything outside the selected tier.
                continue

            if line.startswith("intervals ["):
                # Before moving to the next interval, save the previous
                # one if it contains a real word instead of silence.
                if start is not None and end is not None and text is not None and text != "":
                    rows.append((start, end, text))

                inside_interval = True
                start, end, text = None, None, None
                continue

            if not inside_interval:
                # Ignore tier-level metadata such as xmin/xmax outside intervals.
                continue

            if line.startswith("xmin ="):
                # Start time of the current word interval.
                start = float(line.split("=", 1)[1].strip())
            elif line.startswith("xmax ="):
                # End time of the current word interval.
                end = float(line.split("=", 1)[1].strip())
            elif line.startswith("text ="):
                # Remove extra spaces and lowercase the word so later
                # comparisons are easier across files.
                text = line.split("=", 1)[1].strip().strip('"').strip()
                text = text.lower()

    # Save the last interval after the loop ends.
    if start is not None and end is not None and text is not None and text != "":
        rows.append((start, end, text))

    return rows


def main():
    """Run the extraction script for this assignment and save a CSV file."""
    path = sys.argv[1]
    output_path = str(Path(path).with_suffix(".csv"))

    # In this assignment, the manual gold file uses an empty tier name,
    # while the MAUS word tier is called ORT-MAU.
    if "manual_alignment" in path:
        tier_name = ""
    else:
        tier_name = "ORT-MAU"

    intervals = extract_intervals(path, tier_name)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Keep the output simple for later matching and evaluation.
        writer.writerow(["label", "start", "end"])
        for start, end, label in intervals:
            writer.writerow([label, start, end])

    print(f"saved {len(intervals)} rows to {output_path}")


if __name__ == "__main__":
    main()
