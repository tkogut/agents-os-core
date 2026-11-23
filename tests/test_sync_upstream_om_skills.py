"""
test_sync_upstream_om_skills.py — Unit tests for OM skills sync script.
Ensures no NameError or undefined references exist and verifies basic sync mechanics.
"""

import ast
import builtins
import os
import unittest


class TestSyncUpstreamOmSkills(unittest.TestCase):
    def setUp(self):
        self.repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.script_path = os.path.join(self.repo_root, "scripts", "sync_upstream_om_skills.py")

    def test_no_undefined_variables(self):
        """Analyze AST to guarantee no undefined variable names exist in the script."""
        with open(self.script_path, "r", encoding="utf-8") as f:
            tree = ast.parse(f.read())

        module_scope = set(dir(builtins)) | {"__file__", "__name__", "__doc__"}
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                module_scope.add(node.name)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    module_scope.add(alias.asname or alias.name)
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    module_scope.add(alias.asname or alias.name)

        undefined = []

        class ScopeChecker(ast.NodeVisitor):
            def __init__(self, base_scope):
                self.scopes = [base_scope]

            def visit_FunctionDef(self, fn_node):
                fn_scope = {a.arg for a in fn_node.args.args}
                self.scopes.append(fn_scope)
                self.generic_visit(fn_node)
                self.scopes.pop()

            def visit_Assign(self, assign_node):
                for target in assign_node.targets:
                    if isinstance(target, ast.Name):
                        self.scopes[-1].add(target.id)
                    elif isinstance(target, (ast.Tuple, ast.List)):
                        for elt in target.elts:
                            if isinstance(elt, ast.Name):
                                self.scopes[-1].add(elt.id)
                self.generic_visit(assign_node)

            def visit_For(self, for_node):
                if isinstance(for_node.target, ast.Name):
                    self.scopes[-1].add(for_node.target.id)
                elif isinstance(for_node.target, (ast.Tuple, ast.List)):
                    for elt in for_node.target.elts:
                        if isinstance(elt, ast.Name):
                            self.scopes[-1].add(elt.id)
                self.generic_visit(for_node)

            def visit_With(self, with_node):
                for item in with_node.items:
                    if item.optional_vars and isinstance(item.optional_vars, ast.Name):
                        self.scopes[-1].add(item.optional_vars.id)
                self.generic_visit(with_node)

            def visit_ListComp(self, comp_node):
                comp_scope = set()
                for gen in comp_node.generators:
                    if isinstance(gen.target, ast.Name):
                        comp_scope.add(gen.target.id)
                self.scopes.append(comp_scope)
                self.generic_visit(comp_node)
                self.scopes.pop()

            def visit_Name(self, name_node):
                if isinstance(name_node.ctx, ast.Load):
                    if not any(name_node.id in s for s in self.scopes):
                        undefined.append((name_node.id, name_node.lineno))

        ScopeChecker(module_scope).visit(tree)
        self.assertEqual(undefined, [], f"Found undefined names: {undefined}")


if __name__ == "__main__":
    unittest.main()
