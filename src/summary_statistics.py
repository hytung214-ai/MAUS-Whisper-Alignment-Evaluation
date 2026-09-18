import csv
import statistics
import sys


def read_csv(path):
    """Read the wide-format comparison CSV file."""
    rows = []

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    return rows


def summarize(values):
    """Compute mean, median, and spread for one list of values."""
    return {
        "mean": statistics.mean(values),
        "median": statistics.median(values),
        "spread": statistics.stdev(values) if len(values) > 1 else 0.0,
    }


def collect_stats(rows, system_name):
    """Collect summary statistics for one aligner."""
    columns = [
        "start_error",
        "end_error",
        "start_abs_error",
        "end_abs_error",
    ]

    stats_rows = []

    for column in columns:
        values = [float(row[f"{system_name}_{column}"]) for row in rows]
        stats = summarize(values)

        stats_rows.append(
            {
                "system": system_name,
                "measure": column,
                "mean": stats["mean"],
                "median": stats["median"],
                "spread": stats["spread"],
            }
        )

    return stats_rows


def save_stats(path, rows):
    """Save the summary statistics as a CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["system", "measure", "mean", "median", "spread"])

        for row in rows:
            writer.writerow(
                [
                    row["system"],
                    row["measure"],
                    row["mean"],
                    row["median"],
                    row["spread"],
                ]
            )


def main():
    """Run summary statistics for MAUS and Whisper."""
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    rows = read_csv(input_path)
    stats_rows = collect_stats(rows, "maus") + collect_stats(rows, "whisper")

    save_stats(output_path, stats_rows)

    print(f"saved summary statistics to {output_path}")


if __name__ == "__main__":
    main()
