from parsing import Parser
from time import process_time
import json


def profile_parsers(filename: str) -> None:
    with open(filename, "r") as f:
        parser = Parser(f)

        start = process_time()
        parser.parse()
        end = process_time()

        print(f"MY PARSER: Elapsed time to process {filename}: {end - start} seconds")

    with open(filename, "r") as f:
        start = process_time()
        json.load(f)
        end = process_time()

        print(f"JSON.LOAD: Elapsed time to process {filename}: {end - start} seconds")


if __name__ == "__main__":
    profile_parsers("./64KB.json")
    profile_parsers("./5MB.json")
