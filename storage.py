"""
storage.py - Persistent Storage Module
---------------------------------------
Handles saving and loading financial data to/from a JSON file.
This ensures that all transactions and budget settings are preserved
between sessions so the user does not lose any data.
"""

import json
import os

# ──────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────
DATA_FILE = "finance_data.json"


def get_empty_data():
    """
    Return a dictionary representing the default (empty) data structure
    used throughout the application.

    Parameters:
        None

    Returns:
        dict: A dictionary with keys 'transactions', 'budget_limits',
              'savings_goal', and 'protected_categories', all set to
              their default empty/zero values.
    """
    data = {
        "transactions": [],
        "budget_limits": {},
        "savings_goal": 0.0,
        "protected_categories": ["Rent", "Utilities"]
    }
    return data


def load_data():
    """
    Load financial data from the JSON file on disk. If the file does
    not exist or contains invalid JSON, return the default empty data
    structure instead.

    Parameters:
        None

    Returns:
        dict: The loaded data dictionary, or the default empty data
              if the file is missing or corrupted.
    """
    if not os.path.exists(DATA_FILE):
        print(f"  No existing data file found. Starting fresh.")
        return get_empty_data()

    try:
        file_handle = open(DATA_FILE, "r")
        content = file_handle.read()
        file_handle.close()
        data = json.loads(content)
        transaction_count = len(data.get("transactions", []))
        print(f"  Loaded {transaction_count} transactions from '{DATA_FILE}'.")
        return data
    except (json.JSONDecodeError, KeyError):
        print(f"  Warning: '{DATA_FILE}' is corrupted. Starting fresh.")
        return get_empty_data()


def save_data(data):
    """
    Save the current financial data dictionary to a JSON file on disk.
    The file is written with indentation for human readability.

    Parameters:
        data (dict): The complete data dictionary containing transactions,
                     budget limits, savings goal, and protected categories.

    Returns:
        bool: True if the save was successful, False otherwise.
    """
    try:
        file_handle = open(DATA_FILE, "w")
        json_string = json.dumps(data, indent=2)
        file_handle.write(json_string)
        file_handle.close()
        return True
    except IOError:
        print("  Error: Could not save data to file.")
        return False


def load_sample_data():
    """
    Generate a realistic set of sample transactions spanning 3 months
    (January to March 2026) for demonstration purposes. Includes
    income, various expense categories, budget limits, a savings goal,
    and protected categories. This allows the user (or a professor
    reviewing the project) to instantly explore all features without
    manually entering data.

    Parameters:
        None

    Returns:
        dict: A fully populated data dictionary ready for use.
    """
    sample = get_empty_data()

    # --- Sample transactions: 3 months of realistic student finances ---
    transactions = [
        # January 2026 - Income
        {"type": "income", "amount": 1800.00, "category": "Salary",
         "date": "2026-01-05", "note": "Part-time job"},
        {"type": "income", "amount": 250.00, "category": "Freelance",
         "date": "2026-01-20", "note": "Tutoring sessions"},
        # January 2026 - Expenses
        {"type": "expense", "amount": 650.00, "category": "Rent",
         "date": "2026-01-01", "note": "Monthly rent"},
        {"type": "expense", "amount": 85.00, "category": "Utilities",
         "date": "2026-01-03", "note": "Electricity + water"},
        {"type": "expense", "amount": 320.00, "category": "Food",
         "date": "2026-01-07", "note": "Groceries week 1-2"},
        {"type": "expense", "amount": 180.00, "category": "Food",
         "date": "2026-01-21", "note": "Groceries week 3-4"},
        {"type": "expense", "amount": 55.00, "category": "Transport",
         "date": "2026-01-02", "note": "Monthly metro pass"},
        {"type": "expense", "amount": 40.00, "category": "Entertainment",
         "date": "2026-01-15", "note": "Cinema + dinner out"},
        {"type": "expense", "amount": 75.00, "category": "Clothing",
         "date": "2026-01-25", "note": "Winter jacket sale"},
        {"type": "expense", "amount": 14.99, "category": "Subscriptions",
         "date": "2026-01-01", "note": "Spotify + cloud storage"},

        # February 2026 - Income
        {"type": "income", "amount": 1800.00, "category": "Salary",
         "date": "2026-02-05", "note": "Part-time job"},
        {"type": "income", "amount": 150.00, "category": "Gifts",
         "date": "2026-02-14", "note": "Birthday money"},
        # February 2026 - Expenses
        {"type": "expense", "amount": 650.00, "category": "Rent",
         "date": "2026-02-01", "note": "Monthly rent"},
        {"type": "expense", "amount": 92.00, "category": "Utilities",
         "date": "2026-02-03", "note": "Electricity + water"},
        {"type": "expense", "amount": 290.00, "category": "Food",
         "date": "2026-02-06", "note": "Groceries week 1-2"},
        {"type": "expense", "amount": 210.00, "category": "Food",
         "date": "2026-02-20", "note": "Groceries + eating out"},
        {"type": "expense", "amount": 55.00, "category": "Transport",
         "date": "2026-02-02", "note": "Monthly metro pass"},
        {"type": "expense", "amount": 120.00, "category": "Entertainment",
         "date": "2026-02-22", "note": "Concert tickets"},
        {"type": "expense", "amount": 45.00, "category": "Health",
         "date": "2026-02-10", "note": "Pharmacy"},
        {"type": "expense", "amount": 14.99, "category": "Subscriptions",
         "date": "2026-02-01", "note": "Spotify + cloud storage"},
        {"type": "expense", "amount": 89.00, "category": "Education",
         "date": "2026-02-15", "note": "Online course"},

        # March 2026 - Income
        {"type": "income", "amount": 1800.00, "category": "Salary",
         "date": "2026-03-05", "note": "Part-time job"},
        {"type": "income", "amount": 300.00, "category": "Freelance",
         "date": "2026-03-18", "note": "Website project"},
        # March 2026 - Expenses
        {"type": "expense", "amount": 650.00, "category": "Rent",
         "date": "2026-03-01", "note": "Monthly rent"},
        {"type": "expense", "amount": 78.00, "category": "Utilities",
         "date": "2026-03-03", "note": "Electricity + water"},
        {"type": "expense", "amount": 310.00, "category": "Food",
         "date": "2026-03-08", "note": "Groceries week 1-2"},
        {"type": "expense", "amount": 195.00, "category": "Food",
         "date": "2026-03-22", "note": "Groceries week 3-4"},
        {"type": "expense", "amount": 55.00, "category": "Transport",
         "date": "2026-03-02", "note": "Monthly metro pass"},
        {"type": "expense", "amount": 35.00, "category": "Transport",
         "date": "2026-03-15", "note": "Taxi to airport"},
        {"type": "expense", "amount": 65.00, "category": "Entertainment",
         "date": "2026-03-10", "note": "Bowling + drinks"},
        {"type": "expense", "amount": 14.99, "category": "Subscriptions",
         "date": "2026-03-01", "note": "Spotify + cloud storage"},
    ]

    sample["transactions"] = transactions

    # Pre-set budget limits (slightly tight to trigger the optimizer)
    sample["budget_limits"] = {
        "Food": 400.00,
        "Rent": 650.00,
        "Transport": 60.00,
        "Entertainment": 50.00,
        "Utilities": 100.00,
        "Subscriptions": 20.00,
        "Clothing": 50.00,
        "Health": 40.00,
        "Education": 80.00
    }

    sample["savings_goal"] = 500.00
    sample["protected_categories"] = ["Rent", "Utilities"]

    count = len(transactions)
    print(f"  Loaded {count} sample transactions (Jan-Mar 2026).")
    print(f"  Budget limits and savings goal pre-configured.")
    return sample
