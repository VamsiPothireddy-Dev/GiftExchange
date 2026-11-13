"""Tests for the gift-exchange assignment rules.

Rules under test:
  1. Every employee gives a gift to exactly one person.
  2. Every employee receives a gift.
  3. No self-gifting (A -> A is forbidden).
  4. No swaps (if A -> B then B -> A is forbidden).

Consequence: a valid assignment needs at least 3 distinct employees.
"""

import unittest

from read_employees import assign_gifts, read_employees

EMPLOYEES_CSV = "employees.csv"


def assignment_violations(pairs, employees):
    """Return a list of rule violations for a (giver, receiver) pairing."""
    violations = []
    givers = [g for g, _ in pairs]
    receivers = [r for _, r in pairs]

    if sorted(givers) != sorted(employees):
        violations.append("givers do not match the employee list exactly once each")
    if sorted(receivers) != sorted(employees):
        violations.append("not every employee receives exactly one gift")

    pair_set = set(pairs)
    for giver, receiver in pairs:
        if giver == receiver:
            violations.append(f"{giver} is self-gifting")
        if (receiver, giver) in pair_set:
            violations.append(f"{giver} and {receiver} swap gifts")

    return violations


class TestAssignmentRules(unittest.TestCase):
    """Each rule validated against the real CSV and a generated list."""

    def setUp(self):
        self.names = [e["name"] for e in read_employees(EMPLOYEES_CSV)]

    def assert_valid(self, names):
        pairs = assign_gifts(list(names))
        violations = assignment_violations(pairs, names)
        self.assertEqual(violations, [])
        return pairs

    def test_every_employee_gives_exactly_one_gift(self):
        pairs = assign_gifts(list(self.names))
        self.assertEqual(sorted(g for g, _ in pairs), sorted(self.names))

    def test_every_employee_gets_a_gift(self):
        pairs = assign_gifts(list(self.names))
        self.assertEqual(sorted(r for _, r in pairs), sorted(self.names))

    def test_no_self_gifting(self):
        pairs = assign_gifts(list(self.names))
        self.assertTrue(all(g != r for g, r in pairs))

    def test_no_gift_swaps(self):
        pairs = assign_gifts(list(self.names))
        pair_set = set(pairs)
        self.assertFalse(any((r, g) in pair_set for g, r in pairs))

    def test_full_assignment_is_valid_for_csv(self):
        self.assert_valid(self.names)

    def test_sample_output_shape(self):
        # A -> B -> C -> A is one of only two valid outcomes for 3 people.
        pairs = self.assert_valid(["A", "B", "C"])
        self.assertIn(pairs[0], [("A", "B"), ("A", "C")])

    def test_repeated_runs_stay_valid(self):
        names = [f"Employee {i}" for i in range(50)]
        for _ in range(25):
            self.assert_valid(names)

    def test_input_list_not_mutated(self):
        names = list(self.names)
        snapshot = list(names)
        assign_gifts(names)
        self.assertEqual(names, snapshot)


class TestEdgeCases(unittest.TestCase):
    def test_three_employees_is_minimum_valid(self):
        violations = assignment_violations(assign_gifts(["A", "B", "C"]), ["A", "B", "C"])
        self.assertEqual(violations, [])

    def test_two_employees_impossible(self):
        # A -> B forces B -> A, which is a swap. Must be rejected.
        with self.assertRaises(ValueError):
            assign_gifts(["A", "B"])

    def test_one_employee_impossible(self):
        # Only possible gift is a self-gift. Must be rejected.
        with self.assertRaises(ValueError):
            assign_gifts(["A"])

    def test_no_employees_rejected(self):
        with self.assertRaises(ValueError):
            assign_gifts([])

    def test_duplicate_names_rejected(self):
        with self.assertRaises(ValueError):
            assign_gifts(["A", "B", "C", "A"])


if __name__ == "__main__":
    unittest.main()
