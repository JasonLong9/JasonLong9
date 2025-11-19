# Primary Arithmetic Exercise Generator

Command-line tool to create primary-school friendly arithmetic exercises and grade submitted answers.

## Features

- `-r` range upper bound (required) and `-n` exercise count (default 20, max 10000).
- Natural numbers and proper fractions, parentheses added automatically; intermediate steps avoid negatives and division results stay proper fractions; exercises are deduplicated.
- Writes `Exercises.txt` and `Answers.txt`; grading mode with `-e/-a` produces `Grade.txt`.
- Standard-library only; unit tests cover expression evaluation, generation constraints, and grading.

## Usage

```bash
cd pair-project
# generate 30 exercises within [0, 20)
python -m arithmetic_generator -r 20 -n 30
# grade answers
python -m arithmetic_generator -e Exercises.txt -a Answers.txt
```

Sample output:

```
Correct: 5 (1, 3, 5, 7, 9)
Wrong: 5 (2, 4, 6, 8, 10)
```

## Structure

```
pair-project/
├── arithmetic_generator/
│   ├── cli.py           # CLI entry for generation/grading
│   ├── config.py        # generation config
│   ├── evaluator.py     # expression parsing/evaluation
│   ├── generator.py     # exercise creation and uniqueness
│   └── grader.py        # grading logic
├── tests/               # unittest-based coverage
└── README.md
```

## Tests

From `pair-project`:

```bash
python -m unittest
```

No extra dependencies are required.

