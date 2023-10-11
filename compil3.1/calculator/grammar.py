from ..syntax.syntax import RHS
from ..syntax.parser import Parser
from ..syntax.syntax import Nonterm, Term


def static_nonterm_list():
    return [
        "E", "E1", "T", "T1", "F"
    ]


def static_term_list():
    return [
        "+", "*", "(", ")", "n", "$"
    ]


def static_delta():
    T = GrammarStructure.terms
    N = GrammarStructure.nonterms
    m = len(N)
    n = len(T)
    q = [[RHS.ERROR] * n for _ in range(m)]
    q[0][2] = RHS([Nonterm("T"), Nonterm("E1")])
    q[0][4] = RHS([Nonterm("T"), Nonterm("E1")])
    q[1][0] = RHS([Term("+"), Nonterm("T"), Nonterm("E1")])
    q[1][3] = RHS.EPSILON
    q[1][5] = RHS.EPSILON
    q[2][2] = RHS([Nonterm("F"), Nonterm("T1")])
    q[2][4] = RHS([Nonterm("F"), Nonterm("T1")])
    q[3][0] = RHS.EPSILON
    q[3][1] = RHS([Term("*"), Nonterm("F"), Nonterm("T1")])
    q[3][3] = RHS.EPSILON
    q[3][5] = RHS.EPSILON
    q[4][2] = RHS([Term("("), Nonterm("E"), Term(")")])
    q[4][4] = RHS([Term("n")])
    return q


class GrammarStructure:
    terms = static_term_list()
    nonterms = static_nonterm_list()
    axiom = Nonterm("E")
    q = static_delta()

    @staticmethod
    def get_parser():
        return Parser(GrammarStructure.terms,
                      GrammarStructure.nonterms,
                      GrammarStructure.axiom,
                      GrammarStructure.q)