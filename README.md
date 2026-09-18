# Word-Level Forced Alignment Evaluation

This project compares MAUS and Whisper word boundaries against manual alignment. It reports signed and absolute start/end timing errors for a self-recorded sentence and one sample from the [Buckeye Corpus](https://buckeyecorpus.osu.edu/).

The repository contains the analysis scripts, aggregate results, plots, and report source. It deliberately excludes audio, transcripts, word-level annotations, raw model output, and the course assignment handout. Obtain Buckeye data directly from its distributor and follow its license; its content may not be redistributed by licensees.

## Requirements

Python 3.10 or later, plus:

```bash
pip install -r requirements.txt
```

## Workflow

Place your own authorized inputs under `data/` and model output under `src/maus/` and `src/whisper/`. The expected inputs are MAUS TextGrid, Whisper JSON with word timestamps, and gold `.words` or CSV annotations. The scripts take input and output paths as positional arguments.

```bash
python src/extract_textgrid.py src/maus/example.TextGrid
python src/extract_json.py src/whisper/example.json
python src/extract_words.py data/transcripts/example.words
python src/filter_csv.py data/gold/words_example.csv data/gold/words_example_filtered.csv
python src/maching.py data/gold/words_example_filtered.csv src/maus/maus_example.csv src/whisper/whisper_example.csv results/example_comparison.csv
python src/summary_statistics.py results/example_comparison.csv results/example_summary_statistics.csv
python src/linear_regression.py results/example_comparison.csv results/example_linear_regression.csv
python src/plot_regression.py results/example_comparison.csv results/example_regression_plot.jpg example
```

The extraction scripts derive output filenames from their inputs. Check the generated names before running the matching step. `src/maching.py` retains its original filename for reproducibility.

## Results

The `results/` directory contains aggregate statistics and plots from the original evaluation. The report source is `report_generated.tex`; it refers to the same plots. Word-level comparison CSV files are excluded because they reproduce or closely derive corpus annotations.

## Data and attribution

The Buckeye Corpus is distributed by The Ohio State University for educational and research use under its [content license](https://buckeyecorpus.osu.edu/License.pdf). This repository does not grant rights to that corpus. MAUS and Whisper are separate tools; their output must be generated from data you are authorized to use.
