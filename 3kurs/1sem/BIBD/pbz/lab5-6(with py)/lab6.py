import tkinter as tk
from tkinter import ttk
import mysql.connector

def load_data(table_name, treeview):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="1221",
            database="db"
        )
        cursor = connection.cursor()
        if table_name == "Teacher":
            query = f"SELECT * FROM {table_name} ORDER BY TeacherName ASC"
        else:
            query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()
        for i in treeview.get_children():
            treeview.delete(i)
        for row in data:
            treeview.insert("", "end", values=row)
    except mysql.connector.Error as err:
        print(f"Ошибка при загрузке данных: {err}")

def search_data(table_name, treeview, search_var):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="1221",
            database="db"
        )
        cursor = connection.cursor()
        if table_name == "Teacher":
            query = f"SELECT * FROM {table_name} WHERE TeacherName LIKE %s"
        else:
            query = f"SELECT * FROM {table_name} WHERE Subject LIKE %s"
        cursor.execute(query, (f"%{search_var.get()}%",))
        data = cursor.fetchall()
        connection.close()
        for i in treeview.get_children():
            treeview.delete(i)
        for row in data:
            treeview.insert("", "end", values=row)
    except mysql.connector.Error as err:
        print(f"Ошибка при поиске данных: {err}")

def sort_data(table_name, treeview, sort_var):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="1221",
            database="db"
        )
        cursor = connection.cursor()
        if table_name == "Teacher":
            query = f"SELECT * FROM {table_name} ORDER BY TeacherName {sort_var.get()}"
        else:
            query = f"SELECT * FROM {table_name} ORDER BY Subject {sort_var.get()}"
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()
        for i in treeview.get_children():
            treeview.delete(i)
        for row in data:
            treeview.insert("", "end", values=row)
    except mysql.connector.Error as err:
        print(f"Ошибка при сортировке данных: {err}")


def generate_report(table_name, search_var, sort_var):
    search_criteria = search_var.get()
    sort_criteria = sort_var.get()
    report = f"Отчет\nПоиск: {search_criteria}\nСортировка: {sort_criteria}\n"
    treeview = None
    columns = []  # Добавим переменную для хранения столбцов отчета

    if table_name == "Class":
        report += "Таблица: Class\n\n"
        treeview = treeview1
        columns = ["ClassID", "Subject", "HoursPerWeek"]  # Столбцы для отчета

    elif table_name == "ClassSubject":
        report += "Таблица: ClassSubject\n\n"
        treeview = treeview2
        columns = ["ClassID", "ClassLetter", "Subject", "TeacherID"]  # Столбцы для отчета

    elif table_name == "Teacher":
        report += "Таблица: Teacher\n\n"
        treeview = treeview3
        columns = ["TeacherID", "TeacherName", "Specialization", "Experience"]  # Столбцы для отчета

    # Добавляем заголовки столбцов
    report += "\t".join(columns) + "\n"
    
    for i in treeview.get_children():
        item = treeview.item(i)['values']
        report += "\t".join(map(str, item)) + "\n"

    # Создание окна для отчета
    report_window = tk.Toplevel(root)
    report_window.title("Отчет")

    # Создание текстового виджета для отображения отчета
    report_text = tk.Text(report_window, wrap=tk.WORD, height=25, width=55)
    report_text.pack()
    report_text.insert("1.0", report)
    report_text.config(state=tk.DISABLED)

def execute_query(query, values=()):
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="1221",
        database="db"
    )
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    connection.close()

root = tk.Tk()
root.title("Расписание уроков")

notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Class")

tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="ClassSubject")

tab3 = ttk.Frame(notebook)
notebook.add(tab3, text="Teacher")

# Элементы интерфейса и функции для вкладки "Class"
labels_class = ["ClassID", "Subject", "HoursPerWeek"]
entries_class = []
entry_var_class = []
for label in labels_class:
    i = labels_class.index(label)
    label_widget = tk.Label(tab1, text=label)
    label_widget.grid(row=i, column=0, padx=10, pady=5)
    entry_var_class.append(tk.StringVar())
    entry = tk.Entry(tab1, textvariable=entry_var_class[i])
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries_class.append(entry)

treeview1 = ttk.Treeview(tab1, columns=labels_class, show="headings")
for label in labels_class:
    treeview1.heading(label, text=label)
    treeview1.column(label, width=100)
treeview1.grid(row=len(labels_class), column=0, columnspan=2, padx=10, pady=5)

load_data("Class", treeview1)

search_var1 = tk.StringVar()
search_label1 = tk.Label(tab1, text="Поиск:")
search_label1.grid(row=len(labels_class) + 3, column=0, padx=10, pady=5)
search_entry1 = tk.Entry(tab1, textvariable=search_var1)
search_entry1.grid(row=len(labels_class) + 3, column=1, padx=10, pady=5)
search_button1 = tk.Button(tab1, text="Искать", command=lambda: search_data("Class", treeview1, search_var1))
search_button1.grid(row=len(labels_class) + 4, column=0, padx=10, pady=5)

sort_var1 = tk.StringVar()
sort_var1.set("ASC")
sort_label1 = tk.Label(tab1, text="Сортировка:")
sort_label1.grid(row=len(labels_class) + 5, column=0, padx=10, pady=5)
sort_option1 = tk.OptionMenu(tab1, sort_var1, "ASC", "DESC")
sort_option1.grid(row=len(labels_class) + 5, column=1, padx=10, pady=5)
sort_button1 = tk.Button(tab1, text="Сортировать", command=lambda: sort_data("Class", treeview1, sort_var1))
sort_button1.grid(row=len(labels_class) + 6, column=0, padx=10, pady=5)

report_button1 = tk.Button(tab1, text="Создать отчет", command=lambda: generate_report("Class", search_var1, sort_var1))
report_button1.grid(row=len(labels_class) + 6, column=1, padx=10, pady=5)

# Элементы интерфейса и функции для вкладки "ClassSubject"
labels_class_subject = ["ClassID", "ClassLetter", "Subject", "TeacherID"]
entries_class_subject = []
entry_var_class_subject = []
for label in labels_class_subject:
    i = labels_class_subject.index(label)
    label_widget = tk.Label(tab2, text=label)
    label_widget.grid(row=i, column=0, padx=10, pady=5)
    entry_var_class_subject.append(tk.StringVar())
    entry = tk.Entry(tab2, textvariable=entry_var_class_subject[i])
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries_class_subject.append(entry)

treeview2 = ttk.Treeview(tab2, columns=labels_class_subject, show="headings")
for label in labels_class_subject:
    treeview2.heading(label, text=label)
    treeview2.column(label, width=100)
treeview2.grid(row=len(labels_class_subject), column=0, columnspan=2, padx=10, pady=5)

load_data("ClassSubject", treeview2)

search_var2 = tk.StringVar()
search_label2 = tk.Label(tab2, text="Поиск:")
search_label2.grid(row=len(labels_class_subject) + 3, column=0, padx=10, pady=5)
search_entry2 = tk.Entry(tab2, textvariable=search_var2)
search_entry2.grid(row=len(labels_class_subject) + 3, column=1, padx=10, pady=5)
search_button2 = tk.Button(tab2, text="Искать", command=lambda: search_data("ClassSubject", treeview2, search_var2))
search_button2.grid(row=len(labels_class_subject) + 4, column=0, padx=10, pady=5)

sort_var2 = tk.StringVar()
sort_var2.set("ASC")
sort_label2 = tk.Label(tab2, text="Сортировка:")
sort_label2.grid(row=len(labels_class_subject) + 5, column=0, padx=10, pady=5)
sort_option2 = tk.OptionMenu(tab2, sort_var2, "ASC", "DESC")
sort_option2.grid(row=len(labels_class_subject) + 5, column=1, padx=10, pady=5)
sort_button2 = tk.Button(tab2, text="Сортировать", command=lambda: sort_data("ClassSubject", treeview2, sort_var2))
sort_button2.grid(row=len(labels_class_subject) + 6, column=0, padx=10, pady=5)

report_button2 = tk.Button(tab2, text="Создать отчет", command=lambda: generate_report("ClassSubject", search_var2, sort_var2))
report_button2.grid(row=len(labels_class_subject) + 6, column=1, padx=10, pady=5)

# Элементы интерфейса и функции для вкладки "Teacher"
labels_teacher = ["TeacherID", "TeacherName", "Specialization", "Experience"]
entries_teacher = []
entry_var_teacher = []
for label in labels_teacher:
    i = labels_teacher.index(label)
    label_widget = tk.Label(tab3, text=label)
    label_widget.grid(row=i, column=0, padx=10, pady=5)
    entry_var_teacher.append(tk.StringVar())
    entry = tk.Entry(tab3, textvariable=entry_var_teacher[i])
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries_teacher.append(entry)

treeview3 = ttk.Treeview(tab3, columns=labels_teacher, show="headings")
for label in labels_teacher:
    treeview3.heading(label, text=label)
    treeview3.column(label, width=100)
treeview3.grid(row=len(labels_teacher), column=0, columnspan=2, padx=10, pady=5)

load_data("Teacher", treeview3)

search_var3 = tk.StringVar()
search_label3 = tk.Label(tab3, text="Поиск:")
search_label3.grid(row=len(labels_teacher) + 3, column=0, padx=10, pady=5)
search_entry3 = tk.Entry(tab3, textvariable=search_var3)
search_entry3.grid(row=len(labels_teacher) + 3, column=1, padx=10, pady=5)
search_button3 = tk.Button(tab3, text="Искать", command=lambda: search_data("Teacher", treeview3, search_var3))
search_button3.grid(row=len(labels_teacher) + 4, column=0, padx=10, pady=5)

sort_var3 = tk.StringVar()
sort_var3.set("ASC")
sort_label3 = tk.Label(tab3, text="Сортировка:")
sort_label3.grid(row=len(labels_teacher) + 5, column=0, padx=10, pady=5)
sort_option3 = tk.OptionMenu(tab3, sort_var3, "ASC", "DESC")
sort_option3.grid(row=len(labels_teacher) + 5, column=1, padx=10, pady=5)
sort_button3 = tk.Button(tab3, text="Сортировать", command=lambda: sort_data("Teacher", treeview3, sort_var3))
sort_button3.grid(row=len(labels_teacher) + 6, column=0, padx=10, pady=5)

report_button3 = tk.Button(tab3, text="Создать отчет", command=lambda: generate_report("Teacher", search_var3, sort_var3))
report_button3.grid(row=len(labels_teacher) + 6, column=1, padx=10, pady=5)

root.mainloop()
