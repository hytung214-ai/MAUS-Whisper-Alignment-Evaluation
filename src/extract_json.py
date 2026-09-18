import csv
import json
import string
import sys
from pathlib import Path


def extract_words(path):
    """Extract word intervals from the Whisper JSON file."""
    # Store each extracted word interval as (start, end, text).
    rows = []

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for segment in data["segments"]:
        # Each segment contains a list of word-level timestamps.
        for word in segment["words"]:
            # Remove spaces and punctuation so the labels match the CSV
            # format used in the TextGrid extraction script.
            text = word["word"].strip().lower().strip(string.punctuation)
            rows.append((word["start"], word["end"], text))

    return rows


def main():
    """Run the extraction script for this assignment and save a CSV file."""
    path = sys.argv[1]
    output_path = str(Path(path).with_suffix(".csv"))
    words = extract_words(path)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # Keep the output simple for later matching and evaluation.
        writer.writerow(["label", "start", "end"])
        for start, end, label in words:
            writer.writerow([label, start, end])

    print(f"saved {len(words)} rows to {output_path}")


if __name__ == "__main__":
    main()
