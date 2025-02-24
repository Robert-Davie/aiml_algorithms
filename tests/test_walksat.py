import pytest
from walksat import *


def test_can_get_literal_from_clause():
    literal1 = Literal("A", True)
    clause1 = Clause([literal1])
    assert all([
        clause1.literals[0].name == "A",
        clause1.literals[0].positive == True,
        clause1.literals[0].value == None
    ])


def test_get_symbols_from_clauses():
    literal1 = Literal("A", True)
    literal2 = Literal("B", True)
    literal3 = Literal("C", True)
    literal4 = Literal("A", True)
    clause1 = Clause([literal1, literal2])
    clause2 = Clause([literal3, literal4])
    symbols = get_symbols_from_clauses([clause1, clause2])
    assert symbols == {"A", "B", "C"}


def test_is_clause_satisfied_false():
    literal1 = Literal("A", True, False)
    literal2 = Literal("B", False, True)
    clause1 = Clause([literal1, literal2])
    assert not is_clause_satisfied(clause1)


def test_is_clause_satisifed_true():
    literal1 = Literal("A", True, False)
    literal2 = Literal("B", False, False)
    clause1 = Clause([literal1, literal2])
    assert is_clause_satisfied(clause1)


def test_is_model_satisfied_true():
    literal1 = Literal("A", True, True)
    literal2 = Literal("B", True, False)
    literal3 = Literal("C", True, False)
    literal4 = Literal("A", True, True)
    clause1 = Clause([literal1, literal2])
    clause2 = Clause([literal3, literal4])
    assert is_model_satisfied([clause1, clause2])


def test_is_model_satisfied_not_true():
    literal1 = Literal("A", True, False)
    literal2 = Literal("B", True, True)
    literal3 = Literal("C", True, False)
    literal4 = Literal("A", True, False)
    clause1 = Clause([literal1, literal2])
    clause2 = Clause([literal3, literal4])
    assert not is_model_satisfied([clause1, clause2])
    

def test_get_wrong_clauses():
    literal1 = Literal("A", True, False)
    literal2 = Literal("B", True, True)
    literal3 = Literal("C", True, False)
    literal4 = Literal("A", True, False)
    clause1 = Clause([literal1, literal2])
    clause2 = Clause([literal3, literal4])
    assert get_wrong_clauses([clause1, clause2]) == [clause2]


def test_get_assignments():
    literal1 = Literal("A", True, False)
    literal2 = Literal("B", True, True)
    literal3 = Literal("C", True, False)
    literal4 = Literal("A", True, False)
    clause1 = Clause([literal1, literal2])
    clause2 = Clause([literal3, literal4])
    assert get_assignments([clause1, clause2]) == {"A": False, "B": True, "C": False}


def test_get_assignments_invalid_assignment():
    literal1 = Literal("A", True, True)
    literal2 = Literal("B", True, True)
    literal3 = Literal("C", True, False)
    literal4 = Literal("A", True, False)
    clause1 = Clause([literal1, literal2])
    clause2 = Clause([literal3, literal4])
    with pytest.raises(ValueError):
        get_assignments([clause1, clause2])


def test_get_number_of_satisfied_clauses():
    literal1 = Literal("A", True, False)
    literal2 = Literal("B", False, False)
    literal3 = Literal("C", True, False)
    literal4 = Literal("A", True, False)
    literal5 = Literal("D", True, True)
    literal6 = Literal("E", True, True)
    clause1 = Clause([literal1, literal2])
    clause2 = Clause([literal3, literal4])
    clause3 = Clause([literal5, literal6])
    assert get_number_of_satisfied_clauses([
        clause1,
        clause2,
        clause3,
    ]) == 2


def test_clause_with_two_nots_is_satisfied():
    literal1 = Literal("A", False, False)
    literal2 = Literal("B", False, False)
    assert is_clause_satisfied(Clause([literal1, literal2]))
    assert is_model_satisfied([Clause([literal1, literal2])])

