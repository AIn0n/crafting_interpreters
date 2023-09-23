import argparse


def define_visitor(file, base_name: str, types: list[str]) -> None:
    print(f"class Visitor{base_name}(abc.ABC):", file=file)
    for type_ in types:
        type_name, _ = type_.split(":")
        print(f"  @abc.abstractmethod", file=file)
        print(f"  def visit{type_name}(self, {base_name.lower()}): pass", file=file)


def define_type(file, base_name: str, class_name: str, fields: str) -> None:
    print(f"class {class_name}({base_name}):", file=file)
    # contructor generation
    print(f"  def __init__(self, {fields}):", file=file)

    for field in fields.split(", "):
        print(f"    self.{field} = {field}", file=file)


def define_ast(output_dir: str, base_name: str, types: list[str]) -> None:
    with open(f"{output_dir}/{base_name}.py", "wt") as f:
        # small comments to indicate that this code is generated
        print(f"# code generated by pylox/tools/generate_ast.py", file=f)
        print(f"from visitor_node import Visitor_node", file=f)
        print(f"import abc", file=f)
        # define Expr base class
        print(f"class {base_name}(Visitor_node): pass", file=f)
        define_visitor(f, base_name, types)
        for type_ in types:
            class_name, fields = type_.split(":")
            define_type(f, base_name, class_name, fields)


def main(output: str) -> None:
    define_ast(
        output,
        "Expr",
        [
            "Assign:name, value",
            "Binary:left, operator, right",
            "Call:callee, paren, arguments",
            "Grouping:expression",
            "Literal:value",
            "Logical:left, operator, right",
            "Unary:operator, right",
            "Variable:name",
        ],
    )
    define_ast(
        output,
        "Stmt",
        [
            "Block:statements",
            "Expression:expression",
            "Function:name, params, body",
            "If:condition, then_branch, else_branch",
            "Print:expression",
            "Return:keyword, value",
            "Var:name, initializer",
            "While:condition, body",
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
