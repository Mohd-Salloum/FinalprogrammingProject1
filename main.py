"""
main.py - Personal Finance Manager & Budget Optimizer
------------------------------------------------------
This is the entry point of the application. It displays the main
menu, routes user choices to the appropriate functions, and handles
auto-saving of data after every operation.

How to run:
    python main.py

Authors: Evan Stelder, Guillermo García-Carpintero Fernández, Mohamad Salloum
Course:  Programming for Economists II - IE University
Date:    March 2026
"""

from storage import load_data, save_data, load_sample_data
from finance import (add_income, add_expense, display_summary,
                     view_transactions, delete_transaction, edit_transaction)
from optimizer import (
    set_savings_goal,
    set_category_limits,
    manage_protected_categories,
    detect_overspending,
    suggest_cuts,
    forecast_next_month,
    scenario_simulation
)

# ──────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────
APP_NAME = "Personal Finance Manager & Budget Optimizer"
VERSION = "1.0"


def display_menu():
    """
    Print the main application menu to the console, showing all
    available actions grouped by category.

    Parameters:
        None

    Returns:
        None
    """
    print(f"\n{'=' * 55}")
    print(f"  {APP_NAME}")
    print(f"  Version {VERSION}")
    print(f"{'=' * 55}")
    print()
    print("  --- Transactions ---")
    print("  1.  Add Income")
    print("  2.  Add Expense")
    print("  3.  View All Transactions")
    print("  4.  Edit a Transaction")
    print("  5.  Delete a Transaction")
    print()
    print("  --- Reports ---")
    print("  6.  Financial Summary Dashboard")
    print("  7.  Next Month Forecast")
    print()
    print("  --- Budget Optimizer ---")
    print("  8.  Set Monthly Savings Goal")
    print("  9.  Set Category Budget Limits")
    print("  10. Manage Protected Categories")
    print("  11. Overspending Report")
    print("  12. Optimization Suggestions")
    print("  13. Scenario Simulation (What If?)")
    print()
    print("  --- Utilities ---")
    print("  14. Load Demo Data (sample transactions)")
    print()
    print("  0.  Save & Exit")
    print(f"{'=' * 55}")


def get_menu_choice():
    """
    Prompt the user to enter a menu choice and validate it.
    Accepts integers from 0 to 14.

    Parameters:
        None

    Returns:
        int: The validated menu choice (0-14), or -1 if invalid.
    """
    try:
        choice = int(input("\n  Enter your choice (0-14): "))
        if 0 <= choice <= 14:
            return choice
        else:
            print("  Invalid choice. Please enter a number between 0 and 14.")
            return -1
    except ValueError:
        print("  Invalid input. Please enter a number.")
        return -1


def main():
    """
    The main program loop. Loads data from file, displays the menu,
    handles user input, and auto-saves after every action. Continues
    running until the user chooses to exit.

    Parameters:
        None

    Returns:
        None
    """
    print(f"\n  Welcome to {APP_NAME}!")
    print(f"  Loading your data...\n")

    # Load existing data (or start fresh)
    data = load_data()

    running = True
    while running:
        display_menu()
        choice = get_menu_choice()

        if choice == -1:
            # Invalid input, just show the menu again
            continue

        elif choice == 1:
            data = add_income(data)
            save_data(data)
            print("  (Data auto-saved.)")

        elif choice == 2:
            data = add_expense(data)
            save_data(data)
            print("  (Data auto-saved.)")

        elif choice == 3:
            view_transactions(data)

        elif choice == 4:
            data = edit_transaction(data)
            save_data(data)
            print("  (Data auto-saved.)")

        elif choice == 5:
            data = delete_transaction(data)
            save_data(data)
            print("  (Data auto-saved.)")

        elif choice == 6:
            display_summary(data)

        elif choice == 7:
            forecast_next_month(data)

        elif choice == 8:
            data = set_savings_goal(data)
            save_data(data)
            print("  (Data auto-saved.)")

        elif choice == 9:
            data = set_category_limits(data)
            save_data(data)
            print("  (Data auto-saved.)")

        elif choice == 10:
            data = manage_protected_categories(data)
            save_data(data)
            print("  (Data auto-saved.)")

        elif choice == 11:
            detect_overspending(data)

        elif choice == 12:
            suggest_cuts(data)

        elif choice == 13:
            scenario_simulation(data)

        elif choice == 14:
            confirm = input("  This will replace your current data. "
                            "Continue? (y/n): ").strip().lower()
            if confirm == "y":
                data = load_sample_data()
                save_data(data)
                print("  (Demo data loaded and saved.)")
            else:
                print("  Cancelled.")

        elif choice == 0:
            save_data(data)
            print(f"\n  Data saved to file. Thank you for using {APP_NAME}!")
            print("  Goodbye!\n")
            running = False


# ──────────────────────────────────────────────
# Program entry point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    main()
