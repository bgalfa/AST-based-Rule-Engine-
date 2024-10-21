# rule_engine.py

import re
from typing import Dict, List, Union
from dataclasses import dataclass
from database import RuleDatabase

class RuleEngineError(Exception):
    pass

@dataclass
class Node:
    type: str
    value: Union[str, int, float, None] = None
    left: Union['Node', None] = None
    right: Union['Node', None] = None

class RuleEngine:
    def __init__(self):
        self.operators = {'AND', 'OR'}
        self.comparisons = {'>', '<', '>=', '<=', '=', '!='}
        self.db = RuleDatabase()
        self.valid_attributes = {'age', 'department', 'salary', 'experience'}  # Example attribute catalog

    def create_rule(self, name: str, rule_string: str) -> Node:
        try:
            tokens = self._tokenize(rule_string)
            ast = self._parse(tokens)
            self.db.add_rule(name, rule_string)
            return ast
        except Exception as e:
            raise RuleEngineError(f"Error creating rule: {str(e)}")

    def _tokenize(self, rule_string: str) -> List[str]:
        return re.findall(r'\(|\)|AND|OR|[<>=!]+|\w+|\'[^\']*\'|\d+', rule_string)

    def _parse(self, tokens: List[str]) -> Node:
        def parse_expression():
            if tokens[0] == '(':
                tokens.pop(0)  # Remove opening parenthesis
                node = parse_or()
                tokens.pop(0)  # Remove closing parenthesis
                return node
            else:
                return parse_comparison()

        def parse_or():
            node = parse_and()
            while tokens and tokens[0] == 'OR':
                tokens.pop(0)  # Remove 'OR'
                right = parse_and()
                node = Node(type='operator', value='OR', left=node, right=right)
            return node

        def parse_and():
            node = parse_expression()
            while tokens and tokens[0] == 'AND':
                tokens.pop(0)  # Remove 'AND'
                right = parse_expression()
                node = Node(type='operator', value='AND', left=node, right=right)
            return node

        def parse_comparison():
            left = tokens.pop(0)
            op = tokens.pop(0)
            right = tokens.pop(0)
            return Node(type='operand', value=f"{left} {op} {right}")

        return parse_or()

    def combine_rules(self, rule_names: List[str]) -> Node:
        if not rule_names:
            return None
        
        rules = [self.db.get_rule(name) for name in rule_names]
        if None in rules:
            raise RuleEngineError("One or more rules not found in the database")
        
        if len(rules) == 1:
            return self._parse(self._tokenize(rules[0]))

        combined_ast = self._parse(self._tokenize(rules[0]))
        for rule in rules[1:]:
            rule_ast = self._parse(self._tokenize(rule))
            combined_ast = Node(type='operator', value='AND', left=combined_ast, right=rule_ast)

        return combined_ast

    def evaluate_rule(self, root: Node, data: Dict[str, Union[int, float, str]]) -> bool:
        if root.type == 'operator':
            if root.value == 'AND':
                return self.evaluate_rule(root.left, data) and self.evaluate_rule(root.right, data)
            elif root.value == 'OR':
                return self.evaluate_rule(root.left, data) or self.evaluate_rule(root.right, data)
        elif root.type == 'operand':
            attr, op, value = root.value.split()
            if attr not in self.valid_attributes:
                raise RuleEngineError(f"Invalid attribute: {attr}")
            attr_value = data.get(attr)
            if attr_value is None:
                return False

            parsed_value = self._parse_value(value)
            if not isinstance(attr_value, type(parsed_value)):
                raise RuleEngineError(f"Type mismatch for attribute {attr}")

            if op == '=':
                return attr_value == parsed_value
            elif op == '!=':
                return attr_value != parsed_value
            elif op == '>':
                return attr_value > parsed_value
            elif op == '<':
                return attr_value < parsed_value
            elif op == '>=':
                return attr_value >= parsed_value
            elif op == '<=':
                return attr_value <= parsed_value

        return False

    def _parse_value(self, value: str) -> Union[int, float, str]:
        if value.startswith("'") and value.endswith("'"):
            return value[1:-1]
        try:
            return int(value)
        except ValueError:
            try:
                return float(value)
            except ValueError:
                return value

    def get_all_rules(self) -> List[Dict[str, str]]:
        return self.db.get_all_rules()

    def delete_rule(self, name: str):
        self.db.delete_rule(name)

    def close(self):
        self.db.close()
