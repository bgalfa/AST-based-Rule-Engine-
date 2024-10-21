# cli.py

from rule_engine import RuleEngine, RuleEngineError

def print_menu():
    print("\n--- Rule Engine CLI ---")
    print("1. Create a new rule")
    print("2. List all rules")
    print("3. Evaluate rules")
    print("4. Delete a rule")
    print("5. Exit")
    print("----------------------")

def main():
    engine = RuleEngine()

    while True:
        print_menu()
        choice = int(input("Enter your choice: "))

        if choice == 1:
            name = input("Enter rule name: ")
            rule_string = input("Enter rule string: ")
            try:
                engine.create_rule(name, rule_string)
                print(f"Rule '{name}' created successfully.")
            except RuleEngineError as e:
                print(f"Error: {str(e)}")

        elif choice == 2:
            rules = engine.get_all_rules()
            if rules:
                for rule in rules:
                    print(f"Name: {rule['name']}, Rule: {rule['rule_string']}")
            else:
                print("No rules found.")

        elif choice == 3:
            rule_names = input("Enter rule names to evaluate (comma-separated): ").split(',')
            try:
                combined_ast = engine.combine_rules(rule_names)
                data = {}
                for attr in engine.valid_attributes:
                    value = input(f"Enter value for {attr}: ")
                    data[attr] = int(value) if attr in ['age', 'salary', 'experience'] else value
                result = engine.evaluate_rule(combined_ast, data)
                print(f"Evaluation result: {result}")
            except RuleEngineError as e:
                print(f"Error: {str(e)}")

        elif choice == 4:
            name = input("Enter rule name to delete: ")
            engine.delete_rule(name)
            print(f"Rule '{name}' deleted.")

        elif choice == 5:
            print("Exiting...")
            engine.close()
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()