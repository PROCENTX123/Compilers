import os

from python.calculator.grammar import GrammarStructure
from python.calculator.interpreter import ArithmeticInterpreter
from python.calculator.scanner import ArithmeticScanner


def main():
    expr_src = "data/expr.txt"

    parserArithm = GrammarStructure.getParser()
    scannerArithm = ArithmeticScanner(expr_src)
    parserArithm.topDownParse(scannerArithm)

    parse_graph_file = os.path.join("out_grammar", "expr_parse_graph.dot")
    parserArithm.addFile(parse_graph_file)

    evaluator = ArithmeticInterpreter(parserArithm.getParseTree())
    expression = scannerArithm.getText()
    print(expression.replace("\n", "") + " = " + str(evaluator.getResult()))

if __name__ == "__main__":
    main()