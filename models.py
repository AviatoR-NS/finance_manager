import csv
from datetime import datetime


class Category:
    """Класс для категории (доход или расход)"""
    def __init__(self, name, type_):
        self.name = name
        self.type = type_  # "доход" или "расход"

    def __str__(self):
        return f"{self.name} ({self.type})"


class Transaction:
    """Класс для одной финансовой операции"""
    def __init__(self, category, amount, description="", date=None):
        self.category = category
        self.amount = amount
        self.description = description
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def to_list(self):
        return [self.date, self.category.name, self.category.type, self.amount, self.description]


class FinanceManager:
    """Класс для управления финансами"""
    def __init__(self, filename="data.csv"):
        self.filename = filename
        self.transactions = []
        self.categories = [
            Category("Зарплата", "доход"),
            Category("Покупки", "расход"),
            Category("Еда", "расход"),
            Category("Транспорт", "расход")
        ]
        self.load_data()

    def add_transaction(self, transaction):
        self.transactions.append(transaction)
        self.save_data()

    def save_data(self):
        with open(self.filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Дата", "Категория", "Тип", "Сумма", "Описание"])
            for t in self.transactions:
                writer.writerow(t.to_list())

    def load_data(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                self.transactions = []
                for row in reader:
                    cat = Category(row["Категория"], row["Тип"])
                    t = Transaction(cat, float(row["Сумма"]), row["Описание"], row["Дата"])
                    self.transactions.append(t)
        except FileNotFoundError:
            self.transactions = []

    def analyze(self):
        """Подсчёт суммы по категориям"""
        stats = {}
        for t in self.transactions:
            stats[t.category.name] = stats.get(t.category.name, 0) + float(t.amount)
        return stats
