# Votee_coding_test


## Description
This is an automated Wordle-like puzzle solver written in Python. It connects to the Votee API and uses intelligent filtering strategies to guess 5-letter English words. The solver uses a constraint-based strategy inspired by human Wordle gameplay. After each guess, it processes API feedback (correct, present, absent) to refine the candidate word list. It tracks confirmed letters at exact positions, known letters that must appear elsewhere, and letters ruled out at certain or all positions. Words that don't meet these constraints are filtered out. Among the remaining candidates, it prioritizes guesses with more unique letters to maximize information gain and try to find the correct word.

## Requirements

- Python 3.7+
- `requests`

## Install & Run

```bash
pip install -r requirements.txt
python main.py
