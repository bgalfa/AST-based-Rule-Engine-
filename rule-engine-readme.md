# Rule Engine with AST

A simple 3-tier rule engine application that determines user eligibility based on attributes like age, department, income, and experience using Abstract Syntax Tree (AST) for rule representation.

## Table of Contents
- [Features](#features)
- [System Architecture](#system-architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Design Choices](#design-choices)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Contributing](#contributing)

## Features
- AST-based rule representation
- Dynamic rule creation and modification
- Rule combination capabilities
- Persistent storage of rules using SQLite
- Command-line interface for easy interaction
- Robust error handling and input validation
- Support for multiple attribute types (string, integer, float)

## System Architecture
The application follows a 3-tier architecture:
1. **UI Layer**: Command-line interface (cli.py)
2. **Business Logic Layer**: Rule engine implementation (rule_engine.py)
3. **Data Layer**: SQLite database integration (database.py)

## Prerequisites
- Python 3.7 or higher
- SQLite3 (included in Python standard library)

No additional external dependencies are required as the project uses only Python standard library components.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/rule-engine.git
cd rule-engine
```

2. Verify Python installation:
```bash
python --version
```

3. The application will automatically create a SQLite database file (rule_engine.db) when first run.

## Usage

1. Start the CLI application:
```bash
python cli.py
```

2. Available commands in the CLI:
- Create a new rule (Option 1)
- List all rules (Option 2)
- Evaluate rules (Option 3)
- Delete a rule (Option 4)
- Exit (Option 5)

### Example Rule Creation
```
Enter rule name: sales_rule
Enter rule string: (age > 30 AND department = 'Sales') AND (salary > 50000 OR experience > 5)
```

### Example Rule Evaluation
```
Enter rule names to evaluate: sales_rule
Enter value for age: 32
Enter value for department: Sales
Enter value for salary: 55000
Enter value for experience: 4
```

## Design Choices

1. **AST Implementation**
   - Used a simple Node class with type, value, and left/right children
   - Supports nested expressions and boolean operators (AND, OR)
   - Recursive descent parsing for rule creation

2. **Database Design**
   - SQLite for simplicity and zero-configuration
   - Two tables: rules (for storing rules) and metadata (for application metadata)
   - Rules stored as strings for flexibility and easy modification

3. **Error Handling**
   - Custom RuleEngineError class for specific error cases
   - Validation for attributes and data types
   - Comprehensive error messages for debugging

4. **Code Organization**
   - Separated concerns into three main components (UI, Engine, Database)
   - Modular design for easy extension and modification
   - Clear class and method responsibilities

## Project Structure
```
rule-engine/
├── cli.py           # Command-line interface
├── rule_engine.py   # Core rule engine implementation
├── database.py      # Database operations
├── README.md        # Project documentation
└── rule_engine.db   # SQLite database (created on first run)
```

## API Reference

### RuleEngine Class
```python
create_rule(name: str, rule_string: str) -> Node
combine_rules(rule_names: List[str]) -> Node
evaluate_rule(root: Node, data: Dict[str, Union[int, float, str]]) -> bool
get_all_rules() -> List[Dict[str, str]]
delete_rule(name: str)
```

### RuleDatabase Class
```python
add_rule(name: str, rule_string: str)
get_rule(name: str) -> str
get_all_rules() -> List[Dict[str, Any]]
delete_rule(name: str)
set_metadata(key: str, value: str)
get_metadata(key: str) -> str
```

## Examples

### Simple Rule
```python
rule = "(age > 30 AND department = 'Sales')"
```

### Complex Rule
```python
rule = "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
```

### Data Format
```python
data = {
    "age": 35,
    "department": "Sales",
    "salary": 60000,
    "experience": 3
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Known Limitations
1. Currently supports only AND/OR operators
2. Limited to comparison operations (>, <, >=, <=, =, !=)
3. No support for custom functions in rules
4. Command-line interface only (no web interface)

## Future Enhancements
1. Web-based user interface
2. Support for more complex operators
3. Custom function support in rules
4. Performance optimizations for large rule sets
5. Rule versioning and history tracking
6. Export/import functionality for rules

## Troubleshooting

### Common Issues

1. Database errors:
   - Ensure write permissions in the application directory
   - Check if database file is not locked by another process

2. Parsing errors:
   - Verify rule syntax follows the specified format
   - Check for matching parentheses
   - Ensure operators are correctly spaced

3. Evaluation errors:
   - Verify data types match the rule requirements
   - Check for missing attributes in input data
   - Ensure values are within expected ranges

### Support

For issues, questions, or contributions, please create an issue in the repository or contact the maintainers.
