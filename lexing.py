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

    def lex_bool(self) -> str:
        if (
            len(self.line) >= len(JSON_TRUE)
            and self.line[: len(JSON_TRUE)] == JSON_TRUE
        ):
            self.line = self.line[len(JSON_TRUE) :]
            return JSON_TRUE
        if (
            len(self.line) >= len(JSON_FALSE)
            and self.line[: len(JSON_FALSE)] == JSON_FALSE
        ):
            self.line = self.line[len(JSON_FALSE) :]
            return JSON_FALSE
        return ""

    def lex_null(self) -> str:
        if (
            len(self.line) >= len(JSON_NULL)
            and self.line[: len(JSON_NULL)] == JSON_NULL
        ):
            self.line = self.line[len(JSON_NULL) :]
            return JSON_NULL
        return ""

    def getTok(self) -> str:

        while self.peek() in JSON_WHITESPACE:
            self.nextChar()

        json_bool = self.lex_bool()
        if json_bool:
            return json_bool
        json_null = self.lex_null()
        if json_null:
            return json_null

        self.nextChar()

        if self.curr in JSON_SYNTAX:
            return self.curr
        if self.curr == JSON_QUOTE:
            return self.lex_string()

        json_num = self.lex_number()
        if json_num:
            return json_num

        if self.curr == "EOF":
            return "EOF"

        raise Exception(f"Unexpected character: {self.curr} on line {self.lineNum}")

    def nextChar(self) -> None:
        c = self.peek()
        if c == "\n":
            self.line = self.stream.readline()
            self.lineNum += 1
        elif c:
            self.line = self.line[1:]
        self.curr = c

    def peek(self) -> str:
        if self.line:
            return self.line[0]
        return "EOF"
