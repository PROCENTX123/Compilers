from ..grammar.structure import GrammarStructure
from ..syntax.syntax import Nonterm, RHS, Term

template = '''
import copy

from python.parser import Parser
from python.syntax.syntax import Nonterm, RHS, Term

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
        return {0}

    @staticmethod
    def term_list():
        return {1}

    @staticmethod
    def delta():
        T = copy.deepcopy(GrammarStructure.terms)
        N = copy.deepcopy(GrammarStructure.nonterms)
        m = len(N)
        n = len(T)
        q = [[RHS.ERROR] * n for _ in range(m)]

        {2}
        return q


GrammarStructure.terms = GrammarStructure.term_list()
GrammarStructure.nonterms = GrammarStructure.nonterm_list()
GrammarStructure.q = GrammarStructure.delta()

'''


class GrammarGenerator:
    @staticmethod
    def generate(grammar: GrammarStructure):
        nterm_str = grammar.nonterm_list()
        term_str = grammar.term_list()

        q_str = ''
        for i in range(len(grammar.q)):
            for j in range(len(grammar.q[i])):
                if grammar.q[i][j] != RHS.ERROR:
                    q_str += f'q[{i}][{j}] = RHS(\n'
                    for item in grammar.q[i][j]:
                        if isinstance(item, Term):
                            q_str += f'\tTerm({item.name}),\n'
                        elif isinstance(item, Nonterm):
                            q_str += f'\tNonterm({item.name}),\n'
                    q_str += ')\n'

        return template.format(nterm_str, term_str, q_str)