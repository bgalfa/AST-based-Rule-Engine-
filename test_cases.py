from rule_engine import RuleEngine,RuleEngineError


engine = RuleEngine()

# Test case 1: Create and store rules
engine.create_rule("rule1", "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)")
engine.create_rule("rule2", "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)")

# Test case 2: Retrieve and combine rules
combined_ast = engine.combine_rules(["rule1", "rule2"])
print("Combined AST:", combined_ast)

# Test case 3: Evaluate rules with valid data
test_data = {
    "age": 35,
    "department": "Sales",
    "salary": 60000,
    "experience": 3
}
result = engine.evaluate_rule(combined_ast, test_data)
print("Evaluation result:", result)

# Test case 4: Error handling for invalid attribute
try:
    engine.create_rule("invalid_rule", "invalid_attr > 10")
except RuleEngineError as e:
    print("Error caught:", str(e))

# Test case 5: Error handling for type mismatch
try:
    invalid_data = {
        "age": "thirty",  # Invalid type for age
        "department": "Sales",
        "salary": 60000,
        "experience": 3
    }
    engine.evaluate_rule(combined_ast, invalid_data)
except RuleEngineError as e:
    print("Error caught:", str(e))

# Clean up
engine.close()