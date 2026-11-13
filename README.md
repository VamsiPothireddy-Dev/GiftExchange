# GiftExchange

A simple Python program that reads `employees.csv` into memory as a list.

## Files

- `employees.csv` — employee data (one `name` column)
- `read_employees.py` — loads the CSV into the `Employees` list and prints each entry

## Requirements

- Python 3.x
- No external dependencies (uses only the standard library)

## How to run

```bash
cd /Users/vamsi/git/GiftExchange
python3 read_employees.py
```

Or run it from anywhere:

```bash
python3 /Users/vamsi/git/GiftExchange/read_employees.py
```

Expected output (one dict per line):

```
{'name': 'Alex Johnson'}
{'name': 'Jordan Lee'}
...
```

## How it works

- `read_employees(path)` opens the CSV, parses it with `csv.DictReader`,
  and returns a list of dicts.
- The module-level `Employees` list holds all rows when the script runs.

## Run a single Python file

General syntax:

```bash
python3 <filename.py>
```

Useful flags:

```bash
python3 -i read_employees.py   # run the file, then drop into an interactive shell
python3 -m read_employees     # run a module by name (requires package layout)
```
