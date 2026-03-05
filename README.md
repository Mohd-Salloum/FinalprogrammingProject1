# Personal Finance Manager & Budget Optimizer

A command-line personal finance application built in Python for tracking income and expenses, generating financial summaries, and optimizing budgets.

**Course:** Programming for Economists II — IE University  
**Date:** March 2026


## Features

### Core Functionality
- **Income & Expense Tracking** — Add transactions with amount, category, date, and optional notes
- **Edit & Delete Transactions** — Fix mistakes or remove entries with confirmation prompts
- **Persistent Storage** — All data is saved to a JSON file and auto-loaded on startup
- **Financial Dashboard** — View total income, expenses, net savings, top spending categories with visual bar charts, biggest expense, and monthly breakdowns
- **Input Validation** — All user inputs are validated with `try/except` to prevent crashes
- **Demo Data Loader** — Instantly load 3 months of realistic sample data to explore all features

### Budget Optimizer (Beyond Course)
- **Savings Goals** — Set a monthly savings target and track progress
- **Category Budget Limits** — Define spending limits per category
- **Overspending Detection** — Automatic comparison of actual spending vs. budget limits
- **Optimization Suggestions** — Smart algorithm that recommends specific cuts, respecting protected (essential) categories
- **Next Month Forecast** — Predicts next month's spending based on the last 3 months' average
- **Scenario Simulation** — "What if I reduce Food by 10%?" — see the impact before making changes


## How to Run

1. Make sure Python 3 is installed on your machine.
2. Clone this repository:
   ```
   git clone https://github.com/YOUR_USERNAME/personal-finance-manager.git
   ```
3. Navigate into the project folder:
   ```
   cd personal-finance-manager
   ```
4. Run the program:
   ```
   python main.py
   ```

No external libraries are needed — the project uses only Python's built-in modules (`json`, `os`).


## Project Structure

```
personal-finance-manager/
├── main.py          # Entry point — menu and program loop
├── finance.py       # Core logic — transactions, summaries, reports
├── storage.py       # Persistent storage — save/load JSON
├── optimizer.py     # Budget optimizer — goals, detection, suggestions
├── README.md        # This file
└── .gitignore       # Git ignore rules
```

### Module Responsibilities

| Module | Purpose |
|---|---|
| `main.py` | Menu display, user input routing, auto-save after each action |
| `finance.py` | Adding transactions, computing totals, category breakdowns, monthly reports |
| `storage.py` | Loading data from `finance_data.json`, saving data back to disk |
| `optimizer.py` | Savings goals, budget limits, overspend detection, cut suggestions, forecasting, scenarios |


## Data Format

All financial data is stored in a single `finance_data.json` file with this structure:

```json
{
  "transactions": [
    {
      "type": "expense",
      "amount": 12.50,
      "category": "Food",
      "date": "2026-03-05",
      "note": "sandwich"
    }
  ],
  "budget_limits": {
    "Food": 250.0,
    "Entertainment": 100.0
  },
  "savings_goal": 300.0,
  "protected_categories": ["Rent", "Utilities"]
}
```


## Key Python Concepts Used

- **Lists & Dictionaries** — Core data structures for transactions and category mappings
- **Functions with Docstrings** — Every function is documented with purpose, parameters, and returns
- **File I/O with JSON** — Persistent storage using `json.dumps()` and `json.loads()`
- **Try/Except** — Error handling on all user inputs (amounts, dates, menu choices)
- **Loops** — `while` loops for menus, `for` loops for data processing
- **String Formatting** — f-strings for clean output and formatted reports
- **Tuples** — Used for sorted category rankings
- **Modular Design** — Code split across 4 files with clear separation of concerns


## Team Members

| Member | Contribution |
|---|---|
| Evan | Storage/file handling, data model |
| Mohamad | Financial summaries and reporting |
|Guillhermo | Budget optimizer and scenario simulation |


## Next Steps / Future Improvements

- Add a graphical interface (e.g., with `tkinter`)
- Support multiple currencies with exchange rates
- Add data export to CSV or Excel
- Implement recurring transactions (e.g., monthly rent auto-entry)
- Add visual charts for spending trends
