"""
finance.py - Core Financial Logic Module

Contains all functions for adding transactions (income and expenses),
generating summary statistics, category breakdowns, and monthly reports.
This module operates on the shared data dictionary and never accesses
files directly — that responsibility belongs to storage.py.
"""

# Constants
EXPENSE_CATEGORIES = [
    "Food", "Rent", "Transport", "Utilities", "Entertainment",
    "Health", "Education", "Clothing", "Subscriptions", "Other"
]

INCOME_CATEGORIES = [
    "Salary", "Freelance", "Investments", "Gifts", "Other"
]


# Input helpers
def get_valid_amount(prompt):
    """
    Repeatedly ask the user for a numeric amount until a valid
    positive float is entered.

    Parameters:
        prompt (str): The text displayed to the user.

    Returns:
        float: A positive floating-point number.
    """
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("  Amount must be greater than zero. Try again.")
            else:
                return value
        except ValueError:
            print("  Invalid input. Please enter a number (e.g. 12.50).")


def get_valid_date(prompt):
    """
    Ask the user for a date string in YYYY-MM-DD format. Basic
    validation checks the structure, month range (1-12), and
    day range (1-31).

    Parameters:
        prompt (str): The text displayed to the user.

    Returns:
        str: A date string in YYYY-MM-DD format.
    """
    while True:
        date_str = input(prompt).strip()
        parts = date_str.split("-")
        if len(parts) != 3:
            print("  Invalid format. Please use YYYY-MM-DD (e.g. 2026-03-05).")
            continue
        try:
            year = int(parts[0])
            month = int(parts[1])
            day = int(parts[2])
            if year < 2000 or year > 2100:
                print("  Year seems out of range. Please use a realistic year.")
                continue
            if month < 1 or month > 12:
                print("  Month must be between 01 and 12.")
                continue
            if day < 1 or day > 31:
                print("  Day must be between 01 and 31.")
                continue
            # Reformat to ensure leading zeros
            formatted = f"{year:04d}-{month:02d}-{day:02d}"
            return formatted
        except ValueError:
            print("  Invalid format. Please use YYYY-MM-DD (e.g. 2026-03-05).")


def choose_from_list(options, prompt):
    """
    Display a numbered list of options and ask the user to pick one.
    Keeps asking until a valid choice is made.

    Parameters:
        options (list): A list of strings representing the choices.
        prompt (str): The text shown before the numbered list.

    Returns:
        str: The selected option string.
    """
    print(prompt)
    for i in range(len(options)):
        print(f"  {i + 1}. {options[i]}")
    while True:
        try:
            choice = int(input("  Enter number: "))
            if 1 <= choice <= len(options):
                return options[choice - 1]
            else:
                print(f"  Please enter a number between 1 and {len(options)}.")
        except ValueError:
            print("  Invalid input. Please enter a number.")


# Transaction functions
def add_income(data):
    """
    Prompt the user for income details and append a new income
    transaction to the data dictionary.

    Parameters:
        data (dict): The main data dictionary containing 'transactions'.

    Returns:
        dict: The same data dictionary with the new income appended.
    """
    print("\n--- Add Income ---")
    amount = get_valid_amount("  Amount (EUR): ")
    category = choose_from_list(INCOME_CATEGORIES, "  Select income source:")
    date = get_valid_date("  Date (YYYY-MM-DD): ")
    note = input("  Note (optional, press Enter to skip): ").strip()

    transaction = {
        "type": "income",
        "amount": amount,
        "category": category,
        "date": date,
        "note": note
    }
    data["transactions"].append(transaction)
    print(f"  Income of EUR {amount:.2f} ({category}) added successfully!")
    return data


def add_expense(data):
    """
    Prompt the user for expense details and append a new expense
    transaction to the data dictionary.

    Parameters:
        data (dict): The main data dictionary containing 'transactions'.

    Returns:
        dict: The same data dictionary with the new expense appended.
    """
    print("\n--- Add Expense ---")
    amount = get_valid_amount("  Amount (EUR): ")
    category = choose_from_list(EXPENSE_CATEGORIES, "  Select expense category:")
    date = get_valid_date("  Date (YYYY-MM-DD): ")
    note = input("  Note (optional, press Enter to skip): ").strip()

    transaction = {
        "type": "expense",
        "amount": amount,
        "category": category,
        "date": date,
        "note": note
    }
    data["transactions"].append(transaction)
    print(f"  Expense of EUR {amount:.2f} ({category}) added successfully!")
    return data


# Summary / reporting functions

def compute_totals(transactions):
    """
    Calculate total income, total expenses, and net savings from a
    list of transaction dictionaries.

    Parameters:
        transactions (list): A list of transaction dictionaries.

    Returns:
        tuple: (total_income, total_expenses, net_savings) as floats.
    """
    total_income = 0.0
    total_expenses = 0.0
    for t in transactions:
        if t["type"] == "income":
            total_income = total_income + t["amount"]
        else:
            total_expenses = total_expenses + t["amount"]
    net_savings = total_income - total_expenses
    return (total_income, total_expenses, net_savings)


def spending_by_category(transactions):
    """
    Group all expense transactions by category and sum the amounts.

    Parameters:
        transactions (list): A list of transaction dictionaries.

    Returns:
        dict: A dictionary mapping category names (str) to total
              amounts spent (float).
    """
    category_totals = {}
    for t in transactions:
        if t["type"] == "expense":
            cat = t["category"]
            if cat in category_totals:
                category_totals[cat] = category_totals[cat] + t["amount"]
            else:
                category_totals[cat] = t["amount"]
    return category_totals


def get_top_categories(category_totals, n=5):
    """
    Return the top N spending categories sorted by amount (descending).

    Parameters:
        category_totals (dict): A dictionary of category -> total amount.
        n (int): How many top categories to return. Default is 5.

    Returns:
        list: A list of tuples (category, amount), sorted descending.
    """
    # Convert dict to list of tuples, then sort
    items = []
    for cat in category_totals:
        items.append((cat, category_totals[cat]))

    # Simple selection sort (descending) to avoid using sorted() with key
    for i in range(len(items)):
        max_idx = i
        for j in range(i + 1, len(items)):
            if items[j][1] > items[max_idx][1]:
                max_idx = j
        # Swap
        items[i], items[max_idx] = items[max_idx], items[i]

    # Return top n
    if n < len(items):
        return items[:n]
    return items


def find_biggest_expense(transactions):
    """
    Find and return the single largest expense transaction.

    Parameters:
        transactions (list): A list of transaction dictionaries.

    Returns:
        dict or None: The transaction dictionary with the highest
                      expense amount, or None if no expenses exist.
    """
    biggest = None
    for t in transactions:
        if t["type"] == "expense":
            if biggest is None or t["amount"] > biggest["amount"]:
                biggest = t
    return biggest


def monthly_summary(transactions):
    """
    Group transactions by month (YYYY-MM) and compute income, expenses,
    and net for each month.

    Parameters:
        transactions (list): A list of transaction dictionaries.

    Returns:
        dict: A dictionary where each key is a month string (YYYY-MM)
              and each value is a dictionary with keys 'income',
              'expenses', and 'net'.
    """
    months = {}
    for t in transactions:
        # Extract YYYY-MM from the date string
        month_key = t["date"][:7]
        if month_key not in months:
            months[month_key] = {"income": 0.0, "expenses": 0.0, "net": 0.0}
        if t["type"] == "income":
            months[month_key]["income"] = months[month_key]["income"] + t["amount"]
        else:
            months[month_key]["expenses"] = months[month_key]["expenses"] + t["amount"]

    # Calculate net for each month
    for m in months:
        months[m]["net"] = months[m]["income"] - months[m]["expenses"]

    return months


def display_summary(data):
    """
    Print a complete financial summary dashboard to the console,
    including totals, top spending categories, biggest expense,
    and a month-by-month breakdown.

    Parameters:
        data (dict): The main data dictionary containing 'transactions'.

    Returns:
        None
    """
    transactions = data["transactions"]

    if len(transactions) == 0:
        print("\n  No transactions recorded yet. Add some first!")
        return

    print("\n" + "=" * 55)
    print("           FINANCIAL SUMMARY DASHBOARD")
    print("=" * 55)

    # --- Overall totals ---
    income, expenses, net = compute_totals(transactions)
    print(f"\n  Total Income:    EUR {income:>10.2f}")
    print(f"  Total Expenses:  EUR {expenses:>10.2f}")
    print(f"  ──────────────────────────────")
    if net >= 0:
        print(f"  Net Savings:     EUR {net:>10.2f}  ✓")
    else:
        print(f"  Net Deficit:     EUR {net:>10.2f}  !")

    # --- Top spending categories with bar chart ---
    cat_totals = spending_by_category(transactions)
    top = get_top_categories(cat_totals, 5)
    print(f"\n  Top Spending Categories:")
    print(f"  {'Category':<18} {'Amount':>10}  {'':>20}")
    print(f"  {'-' * 52}")

    # Find the max amount to scale bars proportionally
    max_amount = 0.0
    for cat, amt in top:
        if amt > max_amount:
            max_amount = amt

    max_bar_length = 20  # characters wide
    for cat, amt in top:
        if max_amount > 0:
            bar_length = int((amt / max_amount) * max_bar_length)
        else:
            bar_length = 0
        bar = "#" * bar_length
        print(f"  {cat:<18} EUR {amt:>8.2f}  {bar}")

    # --- Biggest single expense ---
    biggest = find_biggest_expense(transactions)
    if biggest is not None:
        note_text = ""
        if biggest["note"] != "":
            note_text = f" ({biggest['note']})"
        print(f"\n  Biggest Single Expense:")
        print(f"  EUR {biggest['amount']:.2f} in {biggest['category']}"
              f" on {biggest['date']}{note_text}")

    # --- Monthly breakdown ---
    months = monthly_summary(transactions)
    # Sort month keys
    month_keys = list(months.keys())
    month_keys.sort()
    print(f"\n  Monthly Breakdown:")
    print(f"  {'Month':<10} {'Income':>10} {'Expenses':>10} {'Net':>10}")
    print(f"  {'-' * 42}")
    for m in month_keys:
        row = months[m]
        print(f"  {m:<10} {row['income']:>10.2f} {row['expenses']:>10.2f} {row['net']:>10.2f}")

    print("\n" + "=" * 55)


def view_transactions(data):
    """
    Display all recorded transactions in a formatted table.

    Parameters:
        data (dict): The main data dictionary containing 'transactions'.

    Returns:
        None
    """
    transactions = data["transactions"]
    if len(transactions) == 0:
        print("\n  No transactions recorded yet.")
        return

    print(f"\n  {'#':<4} {'Type':<8} {'Category':<15} {'Amount':>10} {'Date':<12} {'Note'}")
    print(f"  {'-' * 65}")
    for i in range(len(transactions)):
        t = transactions[i]
        print(f"  {i+1:<4} {t['type']:<8} {t['category']:<15} "
              f"EUR {t['amount']:>8.2f} {t['date']:<12} {t['note']}")


def delete_transaction(data):
    """
    Display all transactions and let the user delete one by its
    number. Includes a confirmation step to prevent accidental
    deletions.

    Parameters:
        data (dict): The main data dictionary containing 'transactions'.

    Returns:
        dict: The updated data dictionary with the transaction removed,
              or unchanged if the user cancels.
    """
    transactions = data["transactions"]
    if len(transactions) == 0:
        print("\n  No transactions to delete.")
        return data

    view_transactions(data)

    while True:
        try:
            idx = int(input("\n  Enter transaction # to delete (0 to cancel): "))
            if idx == 0:
                print("  Cancelled.")
                return data
            if 1 <= idx <= len(transactions):
                break
            else:
                print(f"  Please enter a number between 1 and {len(transactions)}.")
        except ValueError:
            print("  Invalid input. Please enter a number.")

    target = transactions[idx - 1]
    print(f"\n  About to delete: {target['type']} | {target['category']} | "
          f"EUR {target['amount']:.2f} | {target['date']}")
    confirm = input("  Are you sure? (y/n): ").strip().lower()
    if confirm == "y":
        transactions.pop(idx - 1)
        print("  Transaction deleted.")
    else:
        print("  Cancelled.")
    return data


def edit_transaction(data):
    """
    Display all transactions and let the user edit one by its number.
    The user can update the amount, category, date, or note of the
    selected transaction. Fields left blank keep their current value.

    Parameters:
        data (dict): The main data dictionary containing 'transactions'.

    Returns:
        dict: The updated data dictionary with the edited transaction.
    """
    transactions = data["transactions"]
    if len(transactions) == 0:
        print("\n  No transactions to edit.")
        return data

    view_transactions(data)

    while True:
        try:
            idx = int(input("\n  Enter transaction # to edit (0 to cancel): "))
            if idx == 0:
                print("  Cancelled.")
                return data
            if 1 <= idx <= len(transactions):
                break
            else:
                print(f"  Please enter a number between 1 and {len(transactions)}.")
        except ValueError:
            print("  Invalid input. Please enter a number.")

    target = transactions[idx - 1]
    print(f"\n  Editing: {target['type']} | {target['category']} | "
          f"EUR {target['amount']:.2f} | {target['date']} | {target['note']}")
    print("  (Press Enter to keep the current value)\n")

    # Edit amount
    amount_input = input(f"  New amount (current: {target['amount']:.2f}): ").strip()
    if amount_input != "":
        try:
            new_amount = float(amount_input)
            if new_amount > 0:
                target["amount"] = new_amount
            else:
                print("  Invalid amount, keeping current value.")
        except ValueError:
            print("  Invalid input, keeping current value.")

    # Edit category
    if target["type"] == "expense":
        cat_options = EXPENSE_CATEGORIES
    else:
        cat_options = INCOME_CATEGORIES
    print(f"  Current category: {target['category']}")
    change_cat = input("  Change category? (y/n): ").strip().lower()
    if change_cat == "y":
        target["category"] = choose_from_list(cat_options, "  Select new category:")

    # Edit date
    date_input = input(f"  New date (current: {target['date']}, YYYY-MM-DD): ").strip()
    if date_input != "":
        parts = date_input.split("-")
        if len(parts) == 3:
            try:
                year = int(parts[0])
                month = int(parts[1])
                day = int(parts[2])
                if (2000 <= year <= 2100 and 1 <= month <= 12
                        and 1 <= day <= 31):
                    target["date"] = f"{year:04d}-{month:02d}-{day:02d}"
                else:
                    print("  Invalid date, keeping current value.")
            except ValueError:
                print("  Invalid date, keeping current value.")
        else:
            print("  Invalid format, keeping current value.")

    # Edit note
    note_input = input(f"  New note (current: '{target['note']}'): ").strip()
    if note_input != "":
        target["note"] = note_input

    print("  Transaction updated successfully!")
    return data
