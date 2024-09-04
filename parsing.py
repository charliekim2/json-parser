from lexing import *
from typing import Dict, List


class Parser:
    def __init__(self, fs: io.TextIOBase) -> None:
        self.lexer: Lexer = Lexer(fs)
        self.currTok: str = ""

        self.next()
        if self.currTok != JSON_LEFTBRACE and self.currTok != JSON_LEFTBRACKET:
            raise Exception("Not a valid JSON object")

    def next(self) -> None:
        self.currTok = self.lexer.getTok()

    def parse_list(self) -> List[object]:
        arr = []

        # Consume left bracket
        self.next()
        while self.currTok != JSON_RIGHTBRACKET:
            parsedTok = self.parse()
            arr.append(parsedTok)

            if self.currTok == JSON_COMMA:
                # Consume comma and proceed to next list item
                self.next()
            elif self.currTok != JSON_RIGHTBRACKET:
                raise Exception(
                    f"Expected end of array ] or comma at line {self.lexer.lineNum}"
                )

        # Consume right bracket
        self.next()
        return arr

    def parse_object(self) -> Dict:
        obj = {}

        # Consume left brace
        self.next()
        while self.currTok != JSON_RIGHTBRACE:
            parsedKey = self.parse()

            # JSON keys must be strings
            if type(parsedKey) != str:
                raise Exception(
                    f"Invalid key of type {type(parsedKey)} on line {self.lexer.lineNum}"
                )
            if parsedKey in obj:
                raise Exception(
                    f"Duplicate field {parsedKey} found on line {self.lexer.lineNum}"
                )
            if self.currTok != JSON_COLON:
                raise Exception(
                    f"Expected colon after key {parsedKey} on line {self.lexer.lineNum}"
                )

            # Consume colon and get value
            self.next()
            parsedVal = self.parse()
            obj[parsedKey] = parsedVal

            if self.currTok == JSON_COMMA:
                # Consume comma and proceed to next kvp
                self.next()
            elif self.currTok != JSON_RIGHTBRACE:
                raise Exception(
                    f"Expected end of object or comma at line {self.lexer.lineNum}"
                )

        # Consume right brace
        self.next()
        return obj

    def parse(self):
        if self.currTok == "EOF":
            raise Exception("Nothing to parse")

        if self.currTok == JSON_LEFTBRACKET:
            return self.parse_list()
        if self.currTok == JSON_LEFTBRACE:
            return self.parse_object()
        return self.cast()

    def cast(self):
        tok = ""
        if self.currTok[0] == JSON_QUOTE:
            tok = self.currTok[1:]
        elif self.currTok[0] in JSON_NUMERIC and self.currTok != JSON_NINFINITY:
            try:
                if "." in self.currTok:
                    tok = float(self.currTok)
                else:
                    tok = int(self.currTok)
            except ValueError:
                raise Exception(
                    f"{self.currTok} is an invalid number on line {self.lexer.lineNum}"
                )
            except Exception as e:
                raise e
        elif self.currTok == JSON_TRUE:
            tok = True
        elif self.currTok == JSON_FALSE:
            tok = False
        elif self.currTok == JSON_NULL:
            tok = None
        elif self.currTok == JSON_INFINITY:
            tok = float("inf")
        elif self.currTok == JSON_NINFINITY:
            tok = float("-inf")
        elif self.currTok == JSON_NAN:
            tok = float("nan")
        else:
            # This should never evaluate because the lexer would raise an exception first
            raise Exception(
                f"Error casting token {self.currTok} on line {self.lexer.lineNum}"
            )

        self.next()
        return tok
