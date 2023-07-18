import argparse


def define_type(file, base_name, class_name, fields):
    print(f"class {class_name}({base_name}):", file=file)
    # contructor generation
    print(f"  def __init__(self, {fields}):", file=file)

    for field in fields.split(", "):
        print(f"    self.{field} = {field}", file=file)


def define_ast(output_dir: str, base_name: str, types: list[str]) -> None:
    with open(f"{output_dir}/{base_name}.py", "wt") as f:
        # small comments to indicate that this code is generated
        print(f"# code generated by pylox/tools/generate_ast.py", file=f)
        # define Expr base class
        print(f"class {base_name}: pass", file=f)
        for type_ in types:
            class_name, fields = type_.split(":")
            define_type(f, base_name, class_name, fields)


def main(output: str) -> None:
    define_ast(
        output,
        "Expr",
        [
            "Binary:left, operator, right",
            "Grouping:expression",
            "Literal:value",
            "Unary:operator, right",
        ],
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="ast generator",
        description="generate abstract syntax tree for lox",
    )
    parser.add_argument("-o", "--output", required=True, default="")
    args = parser.parse_args()

    main(args.output)
