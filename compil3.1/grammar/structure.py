import copy

from ..syntax.parser import Parser
from ..syntax.syntax import Nonterm, RHS, Term


class GrammarStructure:
    axiom = Nonterm("S")

    @staticmethod
    def get_parser():
        return Parser(GrammarStructure.terms,
                      GrammarStructure.nonterms,
                      GrammarStructure.axiom,
                      GrammarStructure.q)

    @staticmethod
    def nonterm_list():
        return [
            "S", "DEF", "DN", "NLST", "DT", "TLST", "RLST", "R", "ELST", "E", "SYMLST", "SYM",
            "AXIOM"
        ]

    @staticmethod
    def term_list():
        return [
            "terminal", "non-terminal", ";", ",", "::=", "epsilon", "|", "N", "T", "axiom", "$"
        ]

    @staticmethod
    def delta():
        T = copy.deepcopy(GrammarStructure.terms)
        N = copy.deepcopy(GrammarStructure.nonterms)
        m = len(N)
        n = len(T)
        q = [[RHS.ERROR] * n for _ in range(m)]

        q[0][1] = RHS(
            Nonterm("DEF"),
            Nonterm("RLST"),
            Nonterm("AXIOM")
        )
        q[1][1] = RHS(
            Nonterm("DN"),
            Nonterm("DT")
        )
        q[2][1] = RHS(
            Term("non-terminal"),
            Term("N"),
            Nonterm("NLST"),
            Term(";")
        )
        q[3][2] = RHS.EPSILON
        q[3][3] = RHS(
            Term(","),
            Term("N"),
            Nonterm("NLST")
        )
        q[4][0] = RHS(
            Term("terminal"),
            Term("T"),
            Nonterm("TLST"),
            Term(";")
        )
        q[5][2] = RHS.EPSILON
        q[5][3] = RHS(
            Term(","),
            Term("T"),
            Nonterm("TLST")
        )
        q[6][7] = RHS(
            Nonterm("R"),
            Nonterm("RLST")
        )
        q[6][9] = RHS.EPSILON
        q[7][7] = RHS(
            Term("N"),
            Term("::="),
            Nonterm("E"),
            Nonterm("ELST"),
            Term(";")
        )
        q[8][2] = RHS.EPSILON
        q[8][6] = RHS(
            Term("|"),
            Nonterm("E"),
            Nonterm("ELST")
        )
        q[9][5] = RHS(
            Term("epsilon")
        )
        q[9][7] = RHS(
            Nonterm("SYM"),
            Nonterm("SYMLST")
        )
        q[9][8] = RHS(
            Nonterm("SYM"),
            Nonterm("SYMLST")
        )
        q[10][2] = RHS.EPSILON
        q[10][6] = RHS.EPSILON
        q[10][7] = RHS(
            Nonterm("SYM"),
            Nonterm("SYMLST")
        )
        q[10][8] = RHS(
            Nonterm("SYM"),
            Nonterm("SYMLST")
        )
        q[11][7] = RHS(
            Term("N")
        )
        q[11][8] = RHS(
            Term("T")
        )
        q[12][9] = RHS(
            Term("axiom"),
            Term("N"),
            Term(";")
        )
        return q


GrammarStructure.terms = GrammarStructure.term_list()
GrammarStructure.nonterms = GrammarStructure.nonterm_list()
GrammarStructure.q = GrammarStructure.delta()