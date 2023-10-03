from Analyzer import LexicalAnalyzer

if __name__ == "__main__":
    analyzer = LexicalAnalyzer('text.txt')
    analyzer.analyze()
    analyzer.print()