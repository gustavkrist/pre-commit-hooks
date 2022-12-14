from __future__ import annotations

import argparse
import ast
from typing import Sequence


class NV(ast.NodeVisitor):
    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.success = True

    def visit_Expr(self, node: ast.Expr) -> None:
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
            if node.value.func.id == "print":
                print(f"{self.filename}:{node.lineno}: Print statement")
                self.success = False
        elif (
            isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Attribute)
            and isinstance(node.value.func.value, ast.Name)
        ):
            if node.value.func.value.id == "logger" and node.value.func.attr in [
                "info",
                "debug",
            ]:
                print(f"{self.filename}:{node.lineno}: Logger statement")
                self.success = False


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*")
    args = parser.parse_args(argv)
    success = True
    for filename in args.filenames:
        with open(filename) as f:
            tree = ast.parse(f.read())
        visitor = NV(filename)
        visitor.visit(tree)
        if success:
            success = visitor.success
    return int(not success)


if __name__ == "__main__":
    raise SystemExit(main())
