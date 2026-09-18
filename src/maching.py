import csv
import sys

def read_csv(path):
    """Read one alignment CSV file into a list of word segments."""
    rows = []

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                {
                    "label": row["label"],
                    "start": float(row["start"]),
                    "end": float(row["end"]),
                }
            )

    return rows


def get_overlap(gold_row, pred_row):
    """Compute the time overlap between one gold word and one predicted word."""
    return max(0, min(gold_row["end"], pred_row["end"]) - max(gold_row["start"], pred_row["start"]))


def match_rows(gold_rows, pred_rows):
    """Match one predicted system to the gold file."""
    matches = {}
    used_pred = set()
    skipped = 0

    for i, gold_row in enumerate(gold_rows):
        candidates = []

        for j, pred_row in enumerate(pred_rows):
            if j in used_pred:
                continue

            overlap = get_overlap(gold_row, pred_row)
            if overlap > 0 and gold_row["label"] == pred_row["label"]:
                candidates.append((j, pred_row, overlap))

        if not candidates:
            skipped += 1
            continue

        pred_index, pred_row, overlap = max(candidates, key=lambda x: x[2])

        matches[i] = {
            "label": gold_row["label"],
            "gold_start": gold_row["start"],
            "gold_end": gold_row["end"],
            "pred_start": pred_row["start"],
            "pred_end": pred_row["end"],
            "start_error": pred_row["start"] - gold_row["start"],
            "end_error": pred_row["end"] - gold_row["end"],
            "start_abs_error": abs(pred_row["start"] - gold_row["start"]),
            "end_abs_error": abs(pred_row["end"] - gold_row["end"]),
            "overlap": overlap,
        }
        used_pred.add(pred_index)

    return matches, skipped


def save_matches(path, rows):
    """Save one wide-format CSV file for both systems."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "label",
                "gold_start",
                "gold_end",
                "maus_start",
                "maus_end",
                "maus_start_error",
                "maus_end_error",
                "maus_start_abs_error",
                "maus_end_abs_error",
                "maus_overlap",
                "whisper_start",
                "whisper_end",
                "whisper_start_error",
                "whisper_end_error",
                "whisper_start_abs_error",
                "whisper_end_abs_error",
                "whisper_overlap",
            ]
        )

        for row in rows:
            writer.writerow(
                [
                    row["label"],
                    row["gold_start"],
                    row["gold_end"],
                    row["maus_start"],
                    row["maus_end"],
                    row["maus_start_error"],
                    row["maus_end_error"],
                    row["maus_start_abs_error"],
                    row["maus_end_abs_error"],
                    row["maus_overlap"],
                    row["whisper_start"],
                    row["whisper_end"],
                    row["whisper_start_error"],
                    row["whisper_end_error"],
                    row["whisper_start_abs_error"],
                    row["whisper_end_abs_error"],
                    row["whisper_overlap"],
                ]
            )


def main():
    """Create one wide-format CSV file for gold, MAUS, and Whisper."""
    gold_path = sys.argv[1]
    maus_path = sys.argv[2]
    whisper_path = sys.argv[3]
    output_path = sys.argv[4]

    gold_rows = read_csv(gold_path)
    maus_rows = read_csv(maus_path)
    whisper_rows = read_csv(whisper_path)

    maus_matches, skipped_maus = match_rows(gold_rows, maus_rows)
    whisper_matches, skipped_whisper = match_rows(gold_rows, whisper_rows)

    wide_rows = []

    for i in range(len(gold_rows)):
        if i not in maus_matches or i not in whisper_matches:
            continue

        wide_rows.append(
            {
                "label": gold_rows[i]["label"],
                "gold_start": gold_rows[i]["start"],
                "gold_end": gold_rows[i]["end"],
                "maus_start": maus_matches[i]["pred_start"],
                "maus_end": maus_matches[i]["pred_end"],
                "maus_start_error": maus_matches[i]["start_error"],
                "maus_end_error": maus_matches[i]["end_error"],
                "maus_start_abs_error": maus_matches[i]["start_abs_error"],
                "maus_end_abs_error": maus_matches[i]["end_abs_error"],
                "maus_overlap": maus_matches[i]["overlap"],
                "whisper_start": whisper_matches[i]["pred_start"],
                "whisper_end": whisper_matches[i]["pred_end"],
                "whisper_start_error": whisper_matches[i]["start_error"],
                "whisper_end_error": whisper_matches[i]["end_error"],
                "whisper_start_abs_error": whisper_matches[i]["start_abs_error"],
                "whisper_end_abs_error": whisper_matches[i]["end_abs_error"],
                "whisper_overlap": whisper_matches[i]["overlap"],
            }
        )

    save_matches(output_path, wide_rows)

    print(f"saved {len(wide_rows)} rows to {output_path}")
    print(f"skipped {skipped_maus} rows for MAUS")
    print(f"skipped {skipped_whisper} rows for Whisper")


if __name__ == "__main__":
    main()
