import csv
import sys

import matplotlib.pyplot as plt


def read_rows(path):
    """Read one wide-format comparison CSV file."""
    rows = []

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    return rows


def fit_line(x_values, y_values):
    """Fit a simple least-squares regression line."""
    x_bar = sum(x_values) / len(x_values)
    y_bar = sum(y_values) / len(y_values)

    numerator = 0
    denominator = 0

    for x, y in zip(x_values, y_values):
        numerator += (x - x_bar) * (y - y_bar)
        denominator += (x - x_bar) ** 2

    slope = numerator / denominator
    intercept = y_bar - slope * x_bar

    return intercept, slope


def plot_system(ax, rows, system_name, dataset_name):
    """Plot one regression panel."""
    x_values = []
    y_values = []

    for row in rows:
        x_values.append(float(row["gold_end"]) - float(row["gold_start"]))
        y_values.append(float(row[f"{system_name}_start_error"]))

    intercept, slope = fit_line(x_values, y_values)
    x_line = sorted(x_values)
    y_line = [intercept + slope * x for x in x_line]

    ax.scatter(x_values, y_values, alpha=0.5)
    ax.plot(x_line, y_line, color="red")
    ax.set_title(f"{system_name.upper()}: Start-Time Signed Error vs Gold Duration ({dataset_name})")
    ax.set_xlabel("Gold segment duration")
    ax.set_ylabel("Start-time signed error")


def main():
    """Create one regression figure with MAUS and Whisper panels."""
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    dataset_name = sys.argv[3]

    rows = read_rows(input_path)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    plot_system(axes[0], rows, "maus", dataset_name)
    plot_system(axes[1], rows, "whisper", dataset_name)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    print(f"saved regression figure to {output_path}")


if __name__ == "__main__":
    main()
