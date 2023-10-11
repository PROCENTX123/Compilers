from python.grammar.structure import GrammarStructure
from python.syntax.parser import GrammarScanner
from python.grammar.generator import GrammarGenerator


def main():
    languageSrc = "data/language.txt"
    languageScanner = GrammarScanner(languageSrc)
    languageParser = GrammarStructure.getParser()
    languageParser.topDownParse(languageScanner)
    languageParser.addFile("out_language/parse_graph.dot")

    gr = GrammarInterpreter(languageParser.getParseTree())
    GrammarGenerator.generate(gr.grammar, "out/gr1.py")

    grammarSrc = "data/grammar.txt"
    scanner = GrammarScanner(grammarSrc)
    parser = GrammarStructure.getParser()
    parser.topDownParse(scanner)
    parser.addFile("out_grammar/arithm_parse_graph.dot")
    gr1 = GrammarInterpreter(parser.getParseTree())
    GrammarGenerator.generate(gr1.grammar, "out/gr2.py")


if __name__ == "__main__":
    main()
