from time import process_time
import json
import myjson


def profile_parsers(filename):
    num_iterations = 10
    myparser_total = 0
    jsonload_total = 0

    for _ in range(num_iterations):
        with open(filename, "r") as f:
            start = process_time()
            myjson.load(f)
            end = process_time()

            myparser_total += end - start

        with open(filename, "r") as f:
            start = process_time()
            json.load(f)
            end = process_time()

            jsonload_total += end - start

    print(
        f"MY PARSER: Average time to process {filename}: {round( myparser_total / num_iterations, 4 )} seconds"
    )
    print(
        f"JSON.LOAD: Average time to process {filename}: {round( jsonload_total / num_iterations, 4 )} seconds"
    )


if __name__ == "__main__":
    profile_parsers("./sample/64KB.json")
    profile_parsers("./sample/5MB.json")
