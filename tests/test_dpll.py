import pytest
from dpll import *


def test_dpll_assign():
    literal1 = Literal("A", True, None)
    literal2 = Literal("B", True, None)
    literal3 = Literal("C", True, None)
    literal4 = Literal("A", True, None)
    clause1 = Clause([literal1, literal2])
    clause2 = Clause([literal3, literal4])
    dpll_assign(
        [clause1, clause2],
        {
            "A": True,
            "B": False,
        }
    )
    assert literal1.value == True
    assert literal2.value == False
    assert literal3.value == None
    assert literal4.value == True


def test_is_clause_unsatisfied_none():
    literal1 = Literal("A", True, None)
    literal2 = Literal("B", False, None)
    clause1 = Clause([literal1, literal2])
    assert is_clause_unsatisfied(clause1) == False


def test_is_clause_unsatisfied_false_a():
    literal1 = Literal("A", True, True)
    literal2 = Literal("B", False, None)
    clause1 = Clause([literal1, literal2])
    assert is_clause_unsatisfied(clause1) == False


def test_is_clause_unsatisfied_false_b():
    literal1 = Literal("A", True, None)
    literal2 = Literal("B", False, False)
    clause1 = Clause([literal1, literal2])
    assert is_clause_unsatisfied(clause1) == False


def test_is_clause_unsatisfied_true():
    literal1 = Literal("A", True, False)
    literal2 = Literal("B", False, True)
    clause1 = Clause([literal1, literal2])
    assert is_clause_unsatisfied(clause1) == True


def test_dpll_finds_satisfiable():
    literal_a = Literal("A", True, None)
    literal_b = Literal("B", True, None)
    literal_c = Literal("C", True, None)
    literal_d = Literal("D", True, None)
    literal_e = Literal("E", True, None)
    literal_not_a = Literal("A", False, None)
    literal_not_b = Literal("B", False, None)
    literal_not_c = Literal("C", False, None)
    clause1 = Clause([literal_a, literal_b, literal_not_c, literal_d])
    clause2 = Clause([literal_not_a, literal_b, literal_not_c])
    clause3 = Clause([literal_not_b, literal_not_c])
    clause4 = Clause([literal_e])
    clause5 = Clause([literal_e, literal_c])
    clauses = [clause1, clause2, clause3, clause4, clause5]
    assert is_dpll_satisfiable(clauses)


def test_dpll_fail():
    literal_a = Literal("A", True, None)
    literal_b = Literal("B", True, None)
    literal_c = Literal("C", True, None)
    literal_not_a = Literal("A", False, None)
    literal_not_b = Literal("B", False, None)
    literal_not_c = Literal("C", False, None)
    clause1 = Clause([literal_a, literal_b])
    clause2 = Clause([literal_a, literal_not_b, literal_c])
    clause3 = Clause([literal_not_a, literal_b])
    clause4 = Clause([literal_not_a, literal_not_b, literal_c])
    clause5 = Clause([literal_not_b, literal_not_c])
    assert not is_dpll_satisfiable([
        clause1, 
        clause2,
        clause3,
        clause4,
        clause5,
    ])