from dataclasses import dataclass
import random


@dataclass
class Literal:
    name: str
    positive: bool
    value: bool = None


@dataclass
class Clause:
    literals: list[Literal]


def get_symbols_from_clauses(clauses_in: list[Clause]) -> set[str]:
    symbols = set()
    for clause in clauses_in:
        for literal in clause.literals:
            symbols.add(literal.name)
    return symbols


def random_assign(clauses_in: list[Clause]):
    symbols = get_symbols_from_clauses(clauses_in)
    assignments = dict()
    for symbol in symbols:
        assignments[symbol] = True if random.random() > 0.5 else False
    for clause in clauses_in:
        for literal in clause.literals:
            literal.value = assignments[literal.name]


def is_clause_satisfied(clause_in):
    return any([
        literal.positive == literal.value for literal in clause_in.literals
    ])


def is_model_satisfied(clauses_in):
    return all([
        is_clause_satisfied(clause_in) for clause_in in clauses_in
    ])


def get_number_of_satisfied_clauses(clauses_in):
    return len([
        clause_in for clause_in in clauses_in if is_clause_satisfied(clause_in)
    ])


def get_wrong_clauses(clauses_in):
    return [
        clause_in for clause_in in clauses_in if not is_clause_satisfied(clause_in)
    ]


def get_assignments(clauses_in):
    assignments = dict()
    for clause in clauses_in:
        for literal in clause.literals:
            if literal.name in assignments.keys():
                if literal.value != assignments[literal.name]:
                    raise ValueError
            else:
                assignments[literal.name] = literal.value
    return assignments


def flip_literal(clauses_in, name_in, value_in):
    for clause in clauses_in:
        for literal in clause.literals:
            if literal.name == name_in:
                literal.value = value_in


def set_assignments(clauses_in, assignments):
    for clause in clauses_in:
        for literal in clause.literals:
            literal.value = assignments[literal.name]


def get_flip_satisfied(clauses_in, assignments_in, to_flip):
    set_assignments(clauses_in, assignments_in)
    flip_literal(clauses_in, to_flip, not assignments_in[to_flip])
    return get_number_of_satisfied_clauses(clauses_in)


def maxmimum_flip(clauses_in):
    res = (None, None)
    assignments = get_assignments(clauses_in)
    for name in assignments.items():
        f = get_flip_satisfied(clauses_in, assignments, name)
        if f > res[1]:
            res = (name, f)
    set_assignments(clauses_in, assignments)
    return res


def walksat(
    clauses: list[Clause],
    p: float,
    max_flips: int,
):
    random_assign(clauses)
    for _ in range(max_flips):
        print(f"current assignments: {get_assignments(clauses)}")
        if is_model_satisfied(clauses):
            print("success")
            print(get_assignments(clauses))
            return 0
        corrected_clause = random.choice(get_wrong_clauses(clauses))
        if random.random() <= p:
            flipped_literal = random.choice(corrected_clause.literals)
            flipped_name = flipped_literal.name
            flipped_value = not flipped_literal.value
            flip_literal(clauses, flipped_name, flipped_value)
            print(f"random flip")
        else:
            print(f"maximum flip")
    print("failure: out of flips")
    return 1


if __name__ == "__main__":
    literal_a = Literal("A", True, None)
    literal_b = Literal("B", True, None)
    literal_c = Literal("C", True, None)
    literal_d = Literal("D", True, None)
    literal_e = Literal("E", True, None)
    literal_not_a = Literal("A", False, None)
    literal_not_b = Literal("B", False, None)
    literal_not_c = Literal("C", False, None)
    literal_not_d = Literal("D", False, None)
    literal_not_e = Literal("E", False, None)
    clause1 = Clause([literal_a, literal_b, literal_not_c, literal_d])
    clause2 = Clause([literal_not_a, literal_b, literal_not_c])
    clause3 = Clause([literal_not_b, literal_not_c])
    clause4 = Clause([literal_e])
    clause5 = Clause([literal_e, literal_c])
    clauses = [clause1, clause2, clause3, clause4, clause5]
    
    walksat(clauses, p=0.5 , max_flips=10)