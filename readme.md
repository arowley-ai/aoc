# Advent of Code Challenges 2024

This repository contains my solutions for the [Advent of Code 2024](https://adventofcode.com/2024) challenges. Each folder corresponds to a specific day's puzzle, with Python code implementing the solution.

## Requirements

The only dependency for running the solutions is [`aocd`](https://github.com/wimglenn/advent-of-code-data), which makes fetching input data seamless.

### Installing Dependencies

You can install the `aocd` library via pip:

```bash
pip install aocd
```

### Setting Up
Ensure you have an Advent of Code account and are logged in.
Set up your aocd token:
Log in to the Advent of Code website and retrieve your session token from the browser cookies.
Run the following command to set up the token for aocd:
```bash
export AOC_SESSION=<your-session-token>
```

Alternatively, create a file at ~/.config/aocd/token (or equivalent for your OS) and paste your session token into the file.

### File structure

```yaml
.
├── README.md
├── 2024/
│   ├── 01.py
│   ├── 02.py
│   ├── ...
└── requirements.txt
```