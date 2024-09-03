from parsing import Parser


if __name__ == "__main__":
    with open("test.json", "r") as f:
        parser = Parser(f)

        obj = parser.parse()
        print(obj)
