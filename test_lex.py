from lexing import Lexer


if __name__ == "__main__":
    with open("./sample/test.json", "r") as f:
        lexer = Lexer(f)
        toks = []
        tok = lexer.getTok()

        while tok != "EOF":
            toks.append(tok)
            tok = lexer.getTok()

        print(toks)
