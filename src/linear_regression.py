import csv
import sys
import math

import mpmath as mp


def read_csv(path):
    """Read the wide-format comparison CSV file."""
    rows = []

    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    return rows


def mean(values):
    """Compute the mean of a list of numbers."""
    return sum(values) / len(values)


def t_cdf(t_value, degrees_of_freedom):
    """Compute the CDF of Student's t distribution."""
    if t_value == 0:
        return 0.5

    x = degrees_of_freedom / (degrees_of_freedom + t_value ** 2)
    ibeta = mp.betainc(degrees_of_freedom / 2, 0.5, 0, x, regularized=True)

    if t_value > 0:
        return 1 - 0.5 * ibeta
    return 0.5 * ibeta


def two_tailed_p_value(t_value, degrees_of_freedom):
    """Compute a two-tailed p-value from a t statistic."""
    cdf = t_cdf(abs(t_value), degrees_of_freedom)
    return 2 * (1 - cdf)


def run_regression(rows, system_name):
    """Run a simple linear regression for one aligner."""
    durations = []
    start_errors = []

    for row in rows:
        # The predictor is the gold word duration.
        duration = float(row["gold_end"]) - float(row["gold_start"])
        durations.append(duration)

        # The outcome is the signed start-time error.
        start_errors.append(float(row[f"{system_name}_start_error"]))

    x_bar = mean(durations)
    y_bar = mean(start_errors)

    numerator = 0
    denominator = 0

    for x, y in zip(durations, start_errors):
        numerator += (x - x_bar) * (y - y_bar)
        denominator += (x - x_bar) ** 2

    slope = numerator / denominator
    intercept = y_bar - slope * x_bar

    ss_total = 0
    ss_residual = 0

    for x, y in zip(durations, start_errors):
        predicted_y = intercept + slope * x
        ss_total += (y - y_bar) ** 2
        ss_residual += (y - predicted_y) ** 2

    r_squared = 1 - (ss_residual / ss_total)
    degrees_of_freedom = len(rows) - 2
    residual_variance = ss_residual / degrees_of_freedom
    slope_se = math.sqrt(residual_variance / denominator)
    intercept_se = math.sqrt(residual_variance * (1 / len(rows) + (x_bar ** 2) / denominator))
    slope_t = slope / slope_se
    intercept_t = intercept / intercept_se
    slope_p = float(two_tailed_p_value(slope_t, degrees_of_freedom))
    intercept_p = float(two_tailed_p_value(intercept_t, degrees_of_freedom))

    return {
        "system": system_name,
        "n": len(rows),
        "intercept": intercept,
        "intercept_se": intercept_se,
        "intercept_t": intercept_t,
        "intercept_p": intercept_p,
        "slope": slope,
        "slope_se": slope_se,
        "slope_t": slope_t,
        "slope_p": slope_p,
        "r_squared": r_squared,
    }


def save_results(path, results):
    """Save the regression results as a CSV file."""
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(
            [
                "system",
                "n",
                "intercept",
                "intercept_se",
                "intercept_t",
                "intercept_p",
                "slope",
                "slope_se",
                "slope_t",
                "slope_p",
                "r_squared",
            ]
        )

        for result in results:
            writer.writerow(
                [
                    result["system"],
                    result["n"],
                    result["intercept"],
                    result["intercept_se"],
                    result["intercept_t"],
                    result["intercept_p"],
                    result["slope"],
                    result["slope_se"],
                    result["slope_t"],
                    result["slope_p"],
                    result["r_squared"],
                ]
            )


def main():
    """Run the linear regressions required for the assignment."""
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    rows = read_csv(input_path)
    maus_result = run_regression(rows, "maus")
    whisper_result = run_regression(rows, "whisper")

    save_results(output_path, [maus_result, whisper_result])

    print(f"saved regression results to {output_path}")


if __name__ == "__main__":
    main()
