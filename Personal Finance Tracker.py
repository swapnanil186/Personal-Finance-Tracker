import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox

class PersonalFinanceTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal Finance Tracker")

        # Initialize an empty data structure to store expenses
        self.expenses = []

        # Set default values for monthly salary and monthly budgets
        self.monthly_salary = 0
        self.monthly_budgets = {'groceries': 0, 'entertainment': 0, 'bills': 0}

        # Load existing data
        self.load_data()

        # GUI components
        self.main_frame = tk.Frame(root, bg="#f0f0f0")
        self.main_frame.pack(padx=20, pady=20)

        self.title_label = tk.Label(self.main_frame, text="Personal Finance Tracker", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.input_salary_button = tk.Button(self.main_frame, text="Input Monthly Income", command=self.input_salary, bg="#FF9800", fg="white", padx=10, pady=5)
        self.input_salary_button.grid(row=1, column=0, pady=10)

        self.record_expense_button = tk.Button(self.main_frame, text="Record Expense", command=self.record_expense, bg="#4CAF50", fg="white", padx=10, pady=5)
        self.record_expense_button.grid(row=1, column=1, pady=10)

        self.view_insights_button = tk.Button(self.main_frame, text="View Personal Finance Report", command=self.view_insights, bg="#2196F3", fg="white", padx=10, pady=5)
        self.view_insights_button.grid(row=2, column=0, pady=10)

        self.exit_button = tk.Button(self.main_frame, text="Exit", command=self.root.destroy, bg="#FF0000", fg="white", padx=10, pady=5)
        self.exit_button.grid(row=2, column=1, pady=10)

    def save_data(self):
        with open('expenses.json', 'w') as file:
            json.dump(self.expenses, file)

    def load_data(self):
        try:
            with open('expenses.json', 'r') as file:
                self.expenses = json.load(file)
        except FileNotFoundError:
            self.expenses = []

    def input_salary(self):
        salary_window = tk.Toplevel(self.root)
        salary_window.title("Input Monthly Income")

        salary_label = tk.Label(salary_window, text="Enter Monthly Income (INR):", font=("Helvetica", 12), bg="#f0f0f0")
        salary_label.grid(row=0, column=0, pady=10)

        salary_entry = tk.Entry(salary_window, font=("Helvetica", 12))
        salary_entry.grid(row=0, column=1, pady=10)

        submit_button = tk.Button(salary_window, text="Submit", command=lambda: self.process_salary(salary_entry.get(), salary_window), bg="#FF9800", fg="white", padx=10, pady=5)
        submit_button.grid(row=1, column=0, columnspan=2, pady=10)

    def process_salary(self, salary, window):
        try:
            self.monthly_salary = float(salary)
            if self.monthly_salary > 0:
                self.generate_monthly_budget()
                messagebox.showinfo("Income Input", f"Monthly income set to INR {self.monthly_salary:.2f}")
                window.destroy()
            else:
                messagebox.showerror("Error", "Invalid input. Please enter a valid positive number.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")

    def generate_monthly_budget(self):
        self.monthly_budgets = {'groceries': self.monthly_salary * 0.2, 'entertainment': self.monthly_salary * 0.1, 'bills': self.monthly_salary * 0.3}

    def record_expense(self):
        expense_window = tk.Toplevel(self.root)
        expense_window.title("Record Expense")

        category_label = tk.Label(expense_window, text="Expense Category:", font=("Helvetica", 12), bg="#f0f0f0")
        category_label.grid(row=0, column=0, pady=10)

        category_entry = tk.Entry(expense_window, font=("Helvetica", 12))
        category_entry.grid(row=0, column=1, pady=10)

        amount_label = tk.Label(expense_window, text="Expense Amount:", font=("Helvetica", 12), bg="#f0f0f0")
        amount_label.grid(row=1, column=0, pady=10)

        amount_entry = tk.Entry(expense_window, font=("Helvetica", 12))
        amount_entry.grid(row=1, column=1, pady=10)

        submit_button = tk.Button(expense_window, text="Submit", command=lambda: self.process_expense(category_entry.get(), amount_entry.get(), expense_window), bg="#4CAF50", fg="white", padx=10, pady=5)
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)

    def process_expense(self, category, amount, window):
        try:
            amount = float(amount)
            if category and amount > 0:
                self.record_expense_data(category, amount)
                messagebox.showinfo("Expense Recorded", "Expense recorded successfully!")
                window.destroy()
            else:
                messagebox.showerror("Error", "Invalid input. Please enter valid values.")
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")

    def record_expense_data(self, category, amount):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        expense = {'timestamp': timestamp, 'category': category, 'amount': amount}
        self.expenses.append(expense)
        self.save_data()

    def calculate_total_expense(self):
        return sum(expense['amount'] for expense in self.expenses)

    def calculate_expense_by_category(self, category):
        return sum(expense['amount'] for expense in self.expenses if expense['category'] == category)

    def calculate_remaining_budget(self, category):
        monthly_budget = self.monthly_budgets.get(category, 0)
        category_spending = self.calculate_expense_by_category(category)
        remaining_budget = max(0, monthly_budget - category_spending)
        return remaining_budget

    def detect_bad_expenses(self):
        bad_expenses = [expense for expense in self.expenses if expense['category'] not in ['rent', 'groceries'] and expense['amount'] > self.monthly_salary * 0.01]
        return bad_expenses

    def view_insights(self):
        total_expense = self.calculate_total_expense()
        annual_income = self.monthly_salary * 12
        annual_saving = annual_income - (total_expense * 12)
        bad_expenses = self.detect_bad_expenses()

        insights_window = tk.Toplevel(self.root)
        insights_window.title("Personal Finance Report")

        total_expense_label = tk.Label(insights_window, text=f"Total Expenses: {total_expense:.2f} INR", font=("Helvetica", 12), bg="#f0f0f0")
        total_expense_label.grid(row=0, column=0, pady=10)

        annual_income_label = tk.Label(insights_window, text=f"Annual Income: {annual_income:.2f} INR", font=("Helvetica", 12), bg="#f0f0f0")
        annual_income_label.grid(row=1, column=0, pady=10)

        annual_saving_label = tk.Label(insights_window, text=f"Annual Saving: {annual_saving:.2f} INR", font=("Helvetica", 12), bg="#f0f0f0")
        annual_saving_label.grid(row=2, column=0, pady=10)

        for category in self.monthly_budgets:
            remaining_budget = self.calculate_remaining_budget(category)
            budget_comparison = "within budget" if remaining_budget >= 0 else "over budget"
            category_insight_label = tk.Label(insights_window, text=f"{category.capitalize()}: {remaining_budget:.2f} INR remaining, {budget_comparison}", font=("Helvetica", 12), bg="#f0f0f0")
            category_insight_label.grid(row=len(self.monthly_budgets) + 3, column=0, pady=5)

        if bad_expenses:
            bad_expenses_label = tk.Label(insights_window, text="Bad Expenses Detected (excluding rent and groceries):", font=("Helvetica", 12, "bold"), bg="#f0f0f0")
            bad_expenses_label.grid(row=len(self.monthly_budgets) + 4, column=0, pady=5)

            for index, expense in enumerate(bad_expenses, start=1):
                expense_insight_label = tk.Label(insights_window, text=f"{index}. {expense['category'].capitalize()}: {expense['amount']:.2f} INR", font=("Helvetica", 12), bg="#f0f0f0")
                expense_insight_label.grid(row=len(self.monthly_budgets) + 4 + index, column=0, pady=2)

    def calculate_daily_spending(self):
        today = datetime.now().strftime("%Y-%m-%d")
        today_expenses = [expense['amount'] for expense in self.expenses if expense['timestamp'].startswith(today)]
        return sum(today_expenses)

if __name__ == "__main__":
    root = tk.Tk()
    app = PersonalFinanceTrackerApp(root)
    root.mainloop()
