from lexing import *
from typing import Dict, List


class Parser:
    def __init__(self, fs: io.TextIOBase) -> None:
        self.filestream = fs
        self.lexer = Lexer(self.filestream)

    def parse_array(self) -> List[object]:
        arr = []

        tok = self.lexer.getTok()
        while tok != JSON_RIGHTBRACKET:
            parsedTok = self.parse(tok)
            arr.append(parsedTok)

            tok = self.lexer.getTok()
            if tok == JSON_COMMA:
                tok = self.lexer.getTok()
                continue
            elif tok != JSON_RIGHTBRACKET:
                raise Exception(
                    f"Expected end of array ] or comma at line {self.lexer.lineNum}"
                )

        return arr

    def parse_object(self) -> Dict:
        obj = {}

        tok = self.lexer.getTok()
        while tok != JSON_RIGHTBRACE:
            parsedKey = self.parse(tok)
            # Python cannot hash dicts, arrays, bools...
            if type(parsedKey) not in (str, int, float):
                parsedKey = str(parsedKey)
            if parsedKey in obj:
                raise Exception(
                    f"Duplicate field {parsedKey} found on line {self.lexer.lineNum}"
                )
            if self.lexer.getTok() != JSON_COLON:
                raise Exception(
                    f"Expected colon after key {parsedKey} on line {self.lexer.lineNum}"
                )

            tok = self.lexer.getTok()
            parsedVal = self.parse(tok)
            obj[parsedKey] = parsedVal

            tok = self.lexer.getTok()
            if tok == JSON_COMMA:
                tok = self.lexer.getTok()
            elif tok != JSON_RIGHTBRACE:
                raise Exception(
                    f"Expected end of object or comma at line {self.lexer.lineNum}"
                )

        return obj

    def parse(self, tok="", is_root=False) -> object:
        if not tok:
            return self.parse(self.lexer.getTok(), True)

        if is_root and tok != JSON_LEFTBRACE:
            raise Exception("Not a valid JSON object")

        if tok == JSON_LEFTBRACKET:
            return self.parse_array()
        if tok == JSON_LEFTBRACE:
            return self.parse_object()
        return self.cast(tok)

    def cast(self, tok: str):
        if tok[0] == JSON_QUOTE:
            return tok[1:]
        elif tok[0] in JSON_NUMERIC:
            try:
                if "." in tok:
                    return float(tok)
                return int(tok)
            except ValueError:
                raise Exception(
                    f"{tok} is an invalid number on line {self.lexer.lineNum}"
                )
            except Exception as e:
                raise e
        elif tok == JSON_TRUE:
            return True
        elif tok == JSON_FALSE:
            return False
        elif tok == JSON_NULL:
            return None

        raise Exception(f"Error casting token {tok} on line {self.lexer.lineNum}")
