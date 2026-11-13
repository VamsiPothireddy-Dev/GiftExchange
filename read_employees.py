import csv
import random


def read_employees(path="employees.csv"):
    employees = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            employees.append(row)
    return employees


def assign_gifts(names):
    n = len(names)
    if n != len(set(names)):
        raise ValueError("employee names must be unique")
    if n < 3:
        raise ValueError("gift exchange requires at least 3 employees")
    shuffled = names[:]
    random.shuffle(shuffled)
    gift_to = {shuffled[i]: shuffled[(i + 1) % n] for i in range(n)}
    return [(name, gift_to[name]) for name in names]


def print_table(rows, headers):
    widths = [max(len(h), *(len(r[i]) for r in rows)) for i, h in enumerate(headers)]

    def fmt(cells):
        return " | ".join(c.ljust(w) for c, w in zip(cells, widths))

    print(fmt(headers))
    print("-+-".join("-" * w for w in widths))
    for row in rows:
        print(fmt(row))


if __name__ == "__main__":
    Employees = read_employees()
    names = [e["name"] for e in Employees]
    print_table(assign_gifts(names), ["Employee", "Gifted to"])
