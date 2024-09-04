import io
from constants import *


class Lexer:

    def __init__(self, fs: io.TextIOBase) -> None:
        self.stream = fs
        self.line = self.stream.readline()
        self.lineNum = 1
        self.curr = ""

    def lex_string(self) -> str:
        # parser knows token is string if it starts with "
        json_string = '"'

        self.nextChar()
        while self.curr != JSON_QUOTE and self.curr != "":
            json_string += self.curr
            self.nextChar()

        # EOF before ending quote
        if not self.curr:
            raise Exception("Expected end of string quote")

        return json_string

    def lex_number(self) -> str:
        json_num = ""

        if self.curr not in JSON_NUMERIC:
            return json_num

        json_num += self.curr
        while self.peek() in JSON_NUMERIC:
            json_num += self.peek()
            self.nextChar()

        return json_num

    def lex_const(self) -> str:
        for const in JSON_CONST:
            if len(self.line) >= len(const) and self.line[: len(const)] == const:
                self.line = self.line[len(const) :]
                return const
        return ""

    def getTok(self) -> str:

        while self.peek() in JSON_WHITESPACE:
            self.nextChar()

        json_const = self.lex_const()
        if json_const:
            return json_const

        self.nextChar()
        if self.curr in JSON_SYNTAX:
            return self.curr
        if self.curr == JSON_QUOTE:
            return self.lex_string()

        json_realnum = self.lex_number()
        if json_realnum:
            return json_realnum

        if self.curr == "EOF":
            return "EOF"

        raise Exception(f"Unexpected character: {self.curr} on line {self.lineNum}")

    def nextChar(self) -> None:
        c = self.peek()
        if len(self.line) == 1:
            self.line = self.stream.readline()
            self.lineNum += 1
        elif c:
            self.line = self.line[1:]
        self.curr = c

    def peek(self) -> str:
        if self.line:
            return self.line[0]
        return "EOF"
