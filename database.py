# database.py

import sqlite3
from typing import List, Dict, Any

class RuleDatabase:
    def __init__(self, db_name: str = 'rule_engine.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS rules (
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            rule_string TEXT NOT NULL
        )
        ''')
        
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        ''')
        self.conn.commit()

    def add_rule(self, name: str, rule_string: str):
        self.cursor.execute('INSERT OR REPLACE INTO rules (name, rule_string) VALUES (?, ?)',
                            (name, rule_string))
        self.conn.commit()

    def get_rule(self, name: str) -> str:
        self.cursor.execute('SELECT rule_string FROM rules WHERE name = ?', (name,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def get_all_rules(self) -> List[Dict[str, Any]]:
        self.cursor.execute('SELECT name, rule_string FROM rules')
        return [{'name': row[0], 'rule_string': row[1]} for row in self.cursor.fetchall()]

    def delete_rule(self, name: str):
        self.cursor.execute('DELETE FROM rules WHERE name = ?', (name,))
        self.conn.commit()

    def set_metadata(self, key: str, value: str):
        self.cursor.execute('INSERT OR REPLACE INTO metadata (key, value) VALUES (?, ?)',
                            (key, value))
        self.conn.commit()

    def get_metadata(self, key: str) -> str:
        self.cursor.execute('SELECT value FROM metadata WHERE key = ?', (key,))
        result = self.cursor.fetchone()
        return result[0] if result else None

    def close(self):
        self.conn.close()

# Usage example
if __name__ == "__main__":
    db = RuleDatabase()
    
    # Add rules
    db.add_rule("rule1", "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)")
    db.add_rule("rule2", "((age > 30 AND department = 'Marketing')) AND (salary > 20000 OR experience > 5)")
    
    # Get a specific rule
    print(db.get_rule("rule1"))
    
    # Get all rules
    print(db.get_all_rules())
    
    # Set and get metadata
    db.set_metadata("last_updated", "2023-10-21")
    print(db.get_metadata("last_updated"))
    
    db.close()