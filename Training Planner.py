"""
Training Planner (План тренировок)
Автор: Абдракипов Айрат

GUI-приложение для планирования тренировок с фильтрацией, JSON и Git.
"""

import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime

# -------------------- Константы --------------------
DATA_FILE = "trainings.json"
DATE_FORMAT = "%Y-%m-%d"

# -------------------- Бизнес-логика --------------------
def validate_date(date_str):
    """Проверяет, что дата в формате YYYY-MM-DD и существует."""
    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return True
    except ValueError:
        return False

def validate_duration(duration_str):
    """Проверяет, что длительность — положительное целое число."""
    try:
        val = int(duration_str)
        if val <= 0:
            return False, "Длительность должна быть положительным числом."
        return True, val
    except ValueError:
        return False, "Длительность должна быть целым числом."

def validate_type(type_str):
    """Проверяет, что тип тренировки не пустой."""
    if not type_str.strip():
        return False, "Тип тренировки не может быть пустым."
    return True, type_str.strip()

def load_trainings():
    """Загружает список тренировок из JSON-файла."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, IOError):
        return []

def save_trainings(trainings):
    """Сохраняет список тренировок в JSON-файл."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(trainings, f, ensure_ascii=False, indent=4)

def add_training(trainings, date, type_, duration):
    """Добавляет новую тренировку после валидации. Возвращает (успех, сообщение)."""
    if not validate_date(date):
        return False, "Ошибка: Неверный формат даты. Используйте YYYY-MM-DD."
    
    valid, msg = validate_duration(duration)
    if not valid:
        return False, f"Ошибка: {msg}"
    
    valid, type_clean = validate_type(type_)
    if not valid:
        return False, f"Ошибка: {msg}"
    
    duration_int = int(duration)
    
    training = {
        "date": date,
        "type": type_clean,
        "duration": duration_int
    }
    
    trainings.append(training)
    save_trainings(trainings)
    return True, "Тренировка успешно добавлена!"

def filter_trainings(trainings, date_filter=None, type_filter=None):
    """Фильтрует тренировки по дате и/или типу."""
    filtered = trainings
    
    if date_filter and date_filter.strip():
        filtered = [t for t in filtered if t["date"] == date_filter]
        
    if type_filter and type_filter.strip():
        filtered = [t for t in filtered if t["type"].lower() == type_filter.lower()]
        
    return filtered

# -------------------- GUI --------------------
class TrainingPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner | Абдракипов Айрат")
        self.root.geometry("800x550")
        self.root.resizable(True, True)
        
        # Загружаем данные
        self.trainings = load_trainings()
        
        # Настройка стилей (используем стандартный ttk, чтобы не требовать ttkbootstrap)
        style = ttk.Style()
        style.theme_use("clam")
        
        # --- Фрейм ввода ---
        input_frame = ttk.LabelFrame(self.root, text="Добавить тренировку", padding=15)
        input_frame.pack(fill="x", padx=15, pady=10)
        
        # Дата
        ttk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):", font=("Arial", 10)).grid(
            row=0, column=0, sticky="w", pady=5)
        self.entry_date = ttk.Entry(input_frame, width=25, font=("Arial", 10))
        self.entry_date.grid(row=0, column=1, padx=10, sticky="w")
        self.entry_date.insert(0, datetime.now().strftime(DATE_FORMAT))
        
        # Тип
        ttk.Label(input_frame, text="Тип тренировки:", font=("Arial", 10)).grid(
            row=1, column=0, sticky="w", pady=5)
        self.entry_type = ttk.Entry(input_frame, width=25, font=("Arial", 10))
        self.entry_type.grid(row=1, column=1, padx=10, sticky="w")
        
        # Длительность
        ttk.Label(input_frame, text="Длительность (мин):", font=("Arial", 10)).grid(
            row=2, column=0, sticky="w", pady=5)
        self.entry_duration = ttk.Entry(input_frame, width=25, font=("Arial", 10))
        self.entry_duration.grid(row=2, column=1, padx=10, sticky="w")
        
        # Кнопка добавления
        self.btn_add = ttk.Button(
            input_frame, text="Добавить тренировку", command=self.add_training)
        self.btn_add.grid(row=3, column=0, columnspan=2, pady=10)
        
        # --- Фрейм фильтрации ---
        filter_frame = ttk.LabelFrame(self.root, text="Фильтр", padding=15)
        filter_frame.pack(fill="x", padx=15, pady=10)
        
        # Фильтр по дате
        ttk.Label(filter_frame, text="По дате:", font=("Arial", 10)).grid(
            row=0, column=0, sticky="w", padx=5)
        self.entry_filter_date = ttk.Entry(filter_frame, width=25, font=("Arial", 10))
        self.entry_filter_date.grid(row=0, column=1, padx=10, sticky="w")
        
        # Фильтр по типу
        ttk.Label(filter_frame, text="По типу:", font=("Arial", 10)).grid(
            row=1, column=0, sticky="w", padx=5)
        self.entry_filter_type = ttk.Entry(filter_frame, width=25, font=("Arial", 10))
        self.entry_filter_type.grid(row=1, column=1, padx=10, sticky="w")
        
        # Кнопки фильтрации и сброса
        btn_frame = ttk.Frame(filter_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.btn_filter = ttk.Button(
            btn_frame, text="Применить фильтр", command=self.refresh_table)
        self.btn_filter.pack(side="left", padx=5)
        
        self.btn_reset = ttk.Button(
            btn_frame, text="Сбросить фильтр", command=self.clear_filters)
        self.btn_reset.pack(side="left", padx=5)
        
        # --- Таблица ---
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Определяем столбцы
        columns = ("date", "type", "duration")
        self.tree = ttk.Treeview(
            table_frame, columns=columns, show="headings", height=12)
        
        # Заголовки
        self.tree.heading("date", text="Дата")
        self.tree.heading("type", text="Тип тренировки")
        self.tree.heading("duration", text="Длительность (мин)")
        
        # Настройка ширины столбцов
        self.tree.column("date", width=150, anchor="center")
        self.tree.column("type", width=250, anchor="center")
        self.tree.column("duration", width=150, anchor="center")
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Заполняем таблицу
        self.refresh_table()
    
    def add_training(self):
        """Обработчик кнопки добавления."""
        date = self.entry_date.get()
        type_ = self.entry_type.get()
        duration = self.entry_duration.get()
        
        success, message = add_training(self.trainings, date, type_, duration)
        
        if success:
            messagebox.showinfo("Успех", message)
            self.entry_date.delete(0, tk.END)
            self.entry_date.insert(0, datetime.now().strftime(DATE_FORMAT))
            self.entry_type.delete(0, tk.END)
            self.entry_duration.delete(0, tk.END)
            self.refresh_table()
        else:
            messagebox.showerror("Ошибка", message)
    
    def refresh_table(self):
        """Обновляет таблицу с учётом фильтров."""
        date_f = self.entry_filter_date.get()
        type_f = self.entry_filter_type.get()
        
        filtered = filter_trainings(self.trainings, date_f, type_f)
        
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        for t in filtered:
            self.tree.insert("", "end", values=(t["date"], t["type"], t["duration"]))
    
    def clear_filters(self):
        """Сбрасывает поля фильтрации и обновляет таблицу."""
        self.entry_filter_date.delete(0, tk.END)
        self.entry_filter_type.delete(0, tk.END)
        self.refresh_table()

# -------------------- Точка входа --------------------
def main():
    root = tk.Tk()
    app = TrainingPlannerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()