import tkinter as tk
from tkinter import ttk, messagebox
from models import Transaction, Category, FinanceManager


class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Учёт личных финансов")

        self.manager = FinanceManager()

        # --- Верхняя панель ввода ---
        frame = tk.Frame(root)
        frame.pack(pady=10)

        tk.Label(frame, text="Категория:").grid(row=0, column=0)
        self.category_var = tk.StringVar()
        categories = [c.name for c in self.manager.categories]
        self.category_menu = ttk.Combobox(frame, textvariable=self.category_var, values=categories)
        self.category_menu.grid(row=0, column=1)

        tk.Label(frame, text="Сумма:").grid(row=0, column=2)
        self.amount_entry = tk.Entry(frame)
        self.amount_entry.grid(row=0, column=3)

        tk.Label(frame, text="Описание:").grid(row=0, column=4)
        self.desc_entry = tk.Entry(frame, width=25)
        self.desc_entry.grid(row=0, column=5)

        tk.Button(frame, text="Добавить", command=self.add_transaction).grid(row=0, column=6, padx=5)

        # --- Таблица ---
        self.tree = ttk.Treeview(root, columns=("Дата", "Категория", "Тип", "Сумма", "Описание"), show="headings")
        for col in ("Дата", "Категория", "Тип", "Сумма", "Описание"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        self.tree.pack(pady=10)

        # --- Аналитика ---
        tk.Button(root, text="Показать аналитику", command=self.show_analysis).pack(pady=5)

        self.load_table()

    def load_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for t in self.manager.transactions:
            self.tree.insert("", tk.END, values=t.to_list())

    def add_transaction(self):
        cat_name = self.category_var.get()
        amount = self.amount_entry.get()

        if not cat_name or not amount:
            messagebox.showwarning("Ошибка", "Введите категорию и сумму!")
            return

        try:
            amount = float(amount)
        except ValueError:
            messagebox.showerror("Ошибка", "Сумма должна быть числом!")
            return

        cat_obj = next((c for c in self.manager.categories if c.name == cat_name), Category(cat_name, "расход"))
        t = Transaction(cat_obj, amount, self.desc_entry.get())
        self.manager.add_transaction(t)

        self.amount_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.load_table()

    def show_analysis(self):
        stats = self.manager.analyze()
        result = "\n".join([f"{cat}: {amount:.2f} руб." for cat, amount in stats.items()])
        messagebox.showinfo("Аналитика", result if result else "Нет данных для анализа.")
