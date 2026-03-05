"""
optimizer.py - Budget Optimizer Module
---------------------------------------
This is the "beyond course" feature that makes the project stand out.
It provides:
  1. Budget goal setting (savings goal + per-category limits)
  2. Overspending detection with friendly warnings
  3. Rule-based optimization suggestions (with protected categories)
  4. Forecasting based on historical averages
  5. Scenario simulation ("What if I reduce X by Y%?")
"""

from finance import (
    spending_by_category,
    compute_totals,
    monthly_summary,
    get_valid_amount,
    choose_from_list,
    EXPENSE_CATEGORIES
)


# ──────────────────────────────────────────────
# Budget goal management
# ──────────────────────────────────────────────
def set_savings_goal(data):
    """
    Prompt the user to set a monthly savings goal in EUR.

    Parameters:
        data (dict): The main data dictionary.

    Returns:
        dict: The updated data dictionary with the new savings goal.
    """
    print("\n--- Set Monthly Savings Goal ---")
    current = data.get("savings_goal", 0.0)
    if current > 0:
        print(f"  Current goal: EUR {current:.2f}/month")
    amount = get_valid_amount("  Enter your monthly savings goal (EUR): ")
    data["savings_goal"] = amount
    print(f"  Savings goal set to EUR {amount:.2f}/month.")
    return data


def set_category_limits(data):
    """
    Allow the user to set spending limits for individual expense
    categories. The user can set limits one at a time and stop
    when finished.

    Parameters:
        data (dict): The main data dictionary.

    Returns:
        dict: The updated data dictionary with new budget limits.
    """
    print("\n--- Set Category Budget Limits ---")
    if "budget_limits" not in data:
        data["budget_limits"] = {}

    # Show current limits
    if len(data["budget_limits"]) > 0:
        print("  Current limits:")
        for cat in data["budget_limits"]:
            print(f"    {cat}: EUR {data['budget_limits'][cat]:.2f}")
        print()

    while True:
        category = choose_from_list(EXPENSE_CATEGORIES,
                                    "  Choose a category to set a limit for:")
        limit = get_valid_amount(f"  Monthly limit for {category} (EUR): ")
        data["budget_limits"][category] = limit
        print(f"  Limit for {category} set to EUR {limit:.2f}/month.")

        again = input("  Set another limit? (y/n): ").strip().lower()
        if again != "y":
            break

    return data


def manage_protected_categories(data):
    """
    Allow the user to view and modify the list of protected categories.
    Protected categories receive smaller cut suggestions from the
    optimizer because they are essential expenses.

    Parameters:
        data (dict): The main data dictionary.

    Returns:
        dict: The updated data dictionary.
    """
    print("\n--- Protected Categories ---")
    print("  Protected categories are essential expenses that the")
    print("  optimizer will avoid cutting aggressively.")

    protected = data.get("protected_categories", ["Rent", "Utilities"])

    print(f"\n  Currently protected: {', '.join(protected)}")
    print("\n  Options:")
    print("  1. Add a category to protected list")
    print("  2. Remove a category from protected list")
    print("  3. Go back")

    while True:
        try:
            choice = int(input("  Enter choice: "))
            if choice == 1:
                cat = choose_from_list(EXPENSE_CATEGORIES,
                                       "  Select category to protect:")
                if cat not in protected:
                    protected.append(cat)
                    print(f"  {cat} is now protected.")
                else:
                    print(f"  {cat} is already protected.")
            elif choice == 2:
                if len(protected) == 0:
                    print("  No protected categories to remove.")
                else:
                    cat = choose_from_list(protected,
                                           "  Select category to unprotect:")
                    protected.remove(cat)
                    print(f"  {cat} is no longer protected.")
            elif choice == 3:
                break
            else:
                print("  Please enter 1, 2, or 3.")
        except ValueError:
            print("  Invalid input. Please enter a number.")

    data["protected_categories"] = protected
    return data


# ──────────────────────────────────────────────
# Overspending detection
# ──────────────────────────────────────────────
def detect_overspending(data):
    """
    Compare actual spending per category against the user's budget
    limits and print a report showing which categories are over
    or under budget.

    Parameters:
        data (dict): The main data dictionary.

    Returns:
        dict: A dictionary mapping category names to the amount
              they are over budget (positive = over, negative = under).
    """
    transactions = data["transactions"]
    limits = data.get("budget_limits", {})

    if len(limits) == 0:
        print("\n  No budget limits set. Use 'Set Category Limits' first.")
        return {}

    cat_spending = spending_by_category(transactions)

    print("\n" + "=" * 55)
    print("           OVERSPENDING REPORT")
    print("=" * 55)
    print(f"\n  {'Category':<18} {'Limit':>8} {'Actual':>8} {'Status':>12}")
    print(f"  {'-' * 48}")

    overspend = {}
    for cat in limits:
        limit = limits[cat]
        actual = cat_spending.get(cat, 0.0)
        diff = actual - limit
        overspend[cat] = diff

        if diff > 0:
            status = f"OVER +{diff:.2f}"
        elif diff == 0:
            status = "ON BUDGET"
        else:
            status = f"under {diff:.2f}"

        print(f"  {cat:<18} {limit:>8.2f} {actual:>8.2f} {status:>12}")

    # Highlight biggest leak
    worst_cat = ""
    worst_amount = 0.0
    for cat in overspend:
        if overspend[cat] > worst_amount:
            worst_amount = overspend[cat]
            worst_cat = cat

    if worst_cat != "":
        print(f"\n  Biggest budget leak: {worst_cat} "
              f"(EUR {worst_amount:.2f} over limit)")
    else:
        print(f"\n  Great job! All categories are within budget.")

    print("=" * 55)
    return overspend


# ──────────────────────────────────────────────
# Optimization suggestions
# ──────────────────────────────────────────────
def suggest_cuts(data):
    """
    Analyze the user's spending and suggest specific category cuts
    needed to reach their savings goal. Protected categories receive
    smaller suggested cuts (max 10% reduction). Non-protected
    categories are ranked by overspend amount and receive larger
    suggested cuts.

    Parameters:
        data (dict): The main data dictionary.

    Returns:
        None (prints the optimization plan to the console).
    """
    transactions = data["transactions"]
    savings_goal = data.get("savings_goal", 0.0)
    protected = data.get("protected_categories", [])

    if len(transactions) == 0:
        print("\n  No transactions to analyze. Add some first!")
        return

    if savings_goal <= 0:
        print("\n  No savings goal set. Use 'Set Savings Goal' first.")
        return

    income, expenses, net = compute_totals(transactions)
    shortfall = savings_goal - net

    print("\n" + "=" * 55)
    print("         BUDGET OPTIMIZATION PLAN")
    print("=" * 55)
    print(f"\n  Monthly savings goal:  EUR {savings_goal:>8.2f}")
    print(f"  Current net savings:   EUR {net:>8.2f}")

    if shortfall <= 0:
        print(f"\n  Congratulations! You are already meeting your")
        print(f"  savings goal by EUR {abs(shortfall):.2f}.")
        print("=" * 55)
        return

    print(f"  Shortfall to cover:    EUR {shortfall:>8.2f}")
    print(f"\n  Suggested cuts:")
    print(f"  {'Category':<18} {'Current':>8} {'Suggested Cut':>14} {'Protected'}")
    print(f"  {'-' * 52}")

    cat_spending = spending_by_category(transactions)

    # Build list of categories sorted by spending (highest first)
    cat_list = []
    for cat in cat_spending:
        cat_list.append((cat, cat_spending[cat]))

    # Sort descending by amount
    for i in range(len(cat_list)):
        max_idx = i
        for j in range(i + 1, len(cat_list)):
            if cat_list[j][1] > cat_list[max_idx][1]:
                max_idx = j
        cat_list[i], cat_list[max_idx] = cat_list[max_idx], cat_list[i]

    total_suggested = 0.0
    suggestions = []

    for cat, amount in cat_list:
        if total_suggested >= shortfall:
            break

        is_protected = cat in protected
        remaining_need = shortfall - total_suggested

        if is_protected:
            # Protected: suggest max 10% cut
            max_cut = amount * 0.10
        else:
            # Non-protected: suggest up to 30% cut
            max_cut = amount * 0.30

        # Don't suggest more than what's needed
        if max_cut > remaining_need:
            cut = remaining_need
        else:
            cut = max_cut

        if cut > 0.50:  # Only suggest if meaningful (> EUR 0.50)
            total_suggested = total_suggested + cut
            prot_label = "Yes" if is_protected else "No"
            print(f"  {cat:<18} {amount:>8.2f} {cut:>10.2f}     {prot_label}")
            suggestions.append({"category": cat, "cut": cut})

    print(f"  {'-' * 52}")
    print(f"  {'Total savings from cuts:':<32} EUR {total_suggested:>8.2f}")

    if total_suggested >= shortfall:
        print(f"\n  These cuts would bring you to your savings goal!")
    else:
        gap = shortfall - total_suggested
        print(f"\n  Warning: Even with these cuts, you are still")
        print(f"  EUR {gap:.2f} short. Consider increasing income")
        print(f"  or reviewing your savings goal.")

    print("=" * 55)


# ──────────────────────────────────────────────
# Forecasting
# ──────────────────────────────────────────────
def forecast_next_month(data):
    """
    Estimate next month's spending based on the average of the
    last 3 months of data. This provides a simple but useful
    prediction to help the user plan ahead.

    Parameters:
        data (dict): The main data dictionary.

    Returns:
        None (prints the forecast to the console).
    """
    transactions = data["transactions"]
    if len(transactions) == 0:
        print("\n  No transactions to analyze.")
        return

    months = monthly_summary(transactions)
    month_keys = list(months.keys())
    month_keys.sort()

    if len(month_keys) < 1:
        print("\n  Not enough data to forecast. Keep tracking!")
        return

    # Use last 3 months (or however many are available)
    recent_count = 3
    if len(month_keys) < recent_count:
        recent_count = len(month_keys)

    recent_months = month_keys[-recent_count:]

    avg_income = 0.0
    avg_expenses = 0.0
    avg_cat_spending = {}

    for m in recent_months:
        avg_income = avg_income + months[m]["income"]
        avg_expenses = avg_expenses + months[m]["expenses"]

    avg_income = avg_income / recent_count
    avg_expenses = avg_expenses / recent_count

    # Category-level forecast
    for t in transactions:
        if t["type"] == "expense" and t["date"][:7] in recent_months:
            cat = t["category"]
            if cat in avg_cat_spending:
                avg_cat_spending[cat] = avg_cat_spending[cat] + t["amount"]
            else:
                avg_cat_spending[cat] = t["amount"]

    for cat in avg_cat_spending:
        avg_cat_spending[cat] = avg_cat_spending[cat] / recent_count

    print("\n" + "=" * 55)
    print("         NEXT MONTH FORECAST")
    print(f"    (based on last {recent_count} month(s) average)")
    print("=" * 55)
    print(f"\n  Estimated Income:    EUR {avg_income:>10.2f}")
    print(f"  Estimated Expenses:  EUR {avg_expenses:>10.2f}")
    print(f"  Estimated Net:       EUR {avg_income - avg_expenses:>10.2f}")

    print(f"\n  Estimated Spending by Category:")
    print(f"  {'Category':<18} {'Est. Amount':>12}")
    print(f"  {'-' * 30}")

    # Sort categories by estimated spending
    cat_items = []
    for cat in avg_cat_spending:
        cat_items.append((cat, avg_cat_spending[cat]))
    for i in range(len(cat_items)):
        max_idx = i
        for j in range(i + 1, len(cat_items)):
            if cat_items[j][1] > cat_items[max_idx][1]:
                max_idx = j
        cat_items[i], cat_items[max_idx] = cat_items[max_idx], cat_items[i]

    for cat, amt in cat_items:
        print(f"  {cat:<18} EUR {amt:>10.2f}")

    print("=" * 55)


# ──────────────────────────────────────────────
# Scenario simulation
# ──────────────────────────────────────────────
def scenario_simulation(data):
    """
    Allow the user to simulate a 'what if' scenario: choosing a
    spending category and a percentage reduction, then showing
    how that change would affect their overall finances and
    whether it helps meet the savings goal.

    Parameters:
        data (dict): The main data dictionary.

    Returns:
        None (prints the scenario results to the console).
    """
    transactions = data["transactions"]
    savings_goal = data.get("savings_goal", 0.0)

    if len(transactions) == 0:
        print("\n  No transactions to simulate with.")
        return

    cat_spending = spending_by_category(transactions)
    if len(cat_spending) == 0:
        print("\n  No expense categories found.")
        return

    # Show current spending
    print("\n--- Scenario Simulation ---")
    print("  Current spending by category:")
    active_categories = []
    for cat in cat_spending:
        active_categories.append(cat)
        print(f"    {cat}: EUR {cat_spending[cat]:.2f}")

    # Pick category
    category = choose_from_list(active_categories,
                                "\n  Which category would you like to reduce?")

    # Get percentage
    while True:
        try:
            pct = float(input("  Reduce by what percentage? (e.g. 10 for 10%): "))
            if pct <= 0 or pct > 100:
                print("  Please enter a percentage between 1 and 100.")
            else:
                break
        except ValueError:
            print("  Invalid input. Please enter a number.")

    current_amount = cat_spending[category]
    reduction = current_amount * (pct / 100.0)
    new_amount = current_amount - reduction

    income, expenses, net = compute_totals(transactions)
    new_expenses = expenses - reduction
    new_net = income - new_expenses

    print("\n" + "=" * 55)
    print("         SCENARIO RESULTS")
    print(f"    What if you reduce {category} by {pct:.0f}%?")
    print("=" * 55)
    print(f"\n  {category} spending: EUR {current_amount:.2f} -> EUR {new_amount:.2f}")
    print(f"  Monthly saving:     EUR {reduction:.2f}")
    print(f"\n  Total expenses:     EUR {expenses:.2f} -> EUR {new_expenses:.2f}")
    print(f"  Net savings:        EUR {net:.2f} -> EUR {new_net:.2f}")

    if savings_goal > 0:
        if new_net >= savings_goal:
            surplus = new_net - savings_goal
            print(f"\n  With this change, you WOULD meet your savings goal")
            print(f"  of EUR {savings_goal:.2f} (surplus: EUR {surplus:.2f}).")
        else:
            gap = savings_goal - new_net
            print(f"\n  With this change, you would still be EUR {gap:.2f}")
            print(f"  short of your savings goal of EUR {savings_goal:.2f}.")
    else:
        print(f"\n  (Set a savings goal to see if this scenario meets it.)")

    print("=" * 55)
