from walksat import Literal, Clause, get_symbols_from_clauses, is_model_satisfied, is_clause_satisfied
from copy import deepcopy
import random


def is_dpll_satisfiable(clauses_in):
    return dpll(
        clauses_in,
        get_symbols_from_clauses(clauses_in),
        dict(),
    )


def dpll(clauses_in: list[Clause], literals_available: set[str], model: dict) -> bool:
    print(f"current model: {model}, literals: {literals_available}")
    dpll_assign(clauses_in, model)
    if is_model_satisfied(clauses_in):
        print(f"succesful model = {model}")
        return True
    if is_model_unsatisfied(clauses_in):
        return False
    res2 = find_pure_symbols(clauses_in)
    if res2 != (None, None):
        model[res2[0]] = res2[1]
        literals_available.remove(res2[0])
        return dpll(
            clauses_in, 
            literals_available,
            model,
        )
    res1 = find_unit_clause(clauses_in)
    if res1 != (None, None):
        model[res1[0]] = res1[1]
        literals_available.remove(res1[0])
        return dpll(
            clauses_in, 
            literals_available,
            model,
        )
    p = sorted(list(literals_available))[0]
    new_literals_1 = deepcopy(literals_available)
    new_literals_1.remove(p)
    new_literals_2 = deepcopy(literals_available)
    new_literals_2.remove(p)
    new_model_1 = deepcopy(model)
    new_model_1[p] = True
    new_model_2 = deepcopy(model)
    new_model_2[p] = False
    p_true = dpll(clauses_in, new_literals_1, new_model_1)
    if p_true:
        return True
    p_false = dpll(clauses_in, new_literals_2, new_model_2)
    return p_false


def dpll_assign(clauses_in: list[Clause], assignments_in: dict):
    for clause in clauses_in:
        for literal in clause.literals:
            if literal.name in assignments_in.keys():
                literal.value = assignments_in[literal.name]
            else:
                literal.value = None


def is_model_unsatisfied(clauses_in):
    for clause in clauses_in:
        if is_clause_unsatisfied(clause):
            return True
    return False


def is_clause_unsatisfied(clause_in):
    for literal in clause_in.literals:
        if literal.positive == None:
            return False
        if literal.value == None:
            return False
        if literal.positive == literal.value:
            return False
    return True


def find_unit_clause(clauses_in):
    for clause in clauses_in:
        none_literals = [literal for literal in clause.literals if literal.value == None]
        if len(none_literals) != 1:
            continue
        if is_clause_satisfied(clause) or is_clause_unsatisfied(clause):
            continue
        return none_literals[0].name, none_literals[0].positive
    return None, None


def find_pure_symbols(clauses_in):
    pure_candidates = {}
    for clause in clauses_in:
        if is_clause_satisfied(clause) or is_clause_unsatisfied(clause):
            continue
        for literal in clause.literals:
            if literal.value == None:
                if literal.name in pure_candidates.keys():
                    if pure_candidates[literal.name] != literal.positive:
                        pure_candidates[literal.name] = "X"
                else:
                    pure_candidates[literal.name] = literal.positive
    pure_candidates = {key: value for key, value in pure_candidates.items() if value != "X"}
    if len(pure_candidates) == 0:
        return None, None
    key_out = sorted(pure_candidates.keys())[0]
    return key_out, pure_candidates[key_out]


if __name__ == "__main__":
    l_x = Literal("X", True, None)
    l_y = Literal("Y", True, None)
    l_z = Literal("Z", True, None)
    l_not_x = Literal("X", False, None)
    l_not_y = Literal("Y", False, None)
    l_not_z = Literal("Z", False, None)
    
    res = is_dpll_satisfiable([
        Clause([l_x, l_y, l_z]),
        Clause([l_x, l_not_y, l_not_z]),
        Clause([l_not_x, l_y, l_z]),
        Clause([l_not_x, l_not_y, l_not_z]),
        Clause([l_not_y, l_z]),
        Clause([l_y, l_not_z]),
    ])
    print("is sentence satisfiable?")
    print(res)
