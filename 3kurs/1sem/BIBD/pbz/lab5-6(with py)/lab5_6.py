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

def delete_data(table_name, tree):
    selected_item = tree.selection()
    if selected_item:
        # Получаем значение первичного ключа записи, которую хотим удалить
        primary_key_value = tree.item(selected_item)['values'][0]
        
        # Определяем, какую таблицу мы удаляем, чтобы правильно сформировать запрос
        if table_name == "Class":
            execute_query("DELETE FROM ClassSubject WHERE ClassID = %s", [primary_key_value])
            execute_query("DELETE FROM Class WHERE ClassID = %s", [primary_key_value])
        elif table_name == "ClassSubject":
            execute_query("DELETE FROM ClassSubject WHERE ClassID = %s", [primary_key_value])
        elif table_name == "Teacher":
            execute_query("DELETE FROM Teacher WHERE TeacherID = %s", [primary_key_value])
        
        load_data(table_name, tree)



def add_data(table_name, tree, entry_vars, labels):
    values = [entry_vars[i].get() for i in range(len(entry_vars))]
    query = f"INSERT INTO {table_name} ({', '.join(labels)}) VALUES ({', '.join(['%s' for _ in range(len(entry_vars))])})"
    
    # Проверка, является ли таблица "ClassSubject" и есть ли TeacherID в введенных данных
    if table_name == "ClassSubject" and "TeacherID" in labels:
        teacher_id = entry_vars[labels.index("TeacherID")].get()
        
        # Проверка, существует ли Teacher с указанным TeacherID
        if not teacher_exists(teacher_id):
            # Если Teacher не существует, добавить запись в Teacher
            add_teacher_data(teacher_id)
    
    execute_query(query, values)
    load_data(table_name, tree)

def teacher_exists(teacher_id):
    # Проверить существование Teacher по TeacherID
    query = "SELECT * FROM Teacher WHERE TeacherID = %s"
    result = execute_query(query, (teacher_id,), fetchone=True)
    return result is not None

def add_teacher_data(teacher_id):
    # Добавить запись в Teacher
    query = "INSERT INTO Teacher (TeacherID) VALUES (%s)"
    execute_query(query, (teacher_id,))


def edit_data(table_name, tree, entry_vars, labels):
    selected_item = tree.selection()
    if selected_item:
        values = [entry_vars[i].get() for i in range(len(entry_vars))]
        # Добавляем ClassID в конец списка значений
        values.append(tree.item(selected_item)['values'][0])
        
        if table_name == "Class":
            query = f"UPDATE {table_name} SET {', '.join([f'{col} = %s' for col in labels])} WHERE ClassID = %s"
        elif table_name == "ClassSubject":
            query = f"UPDATE {table_name} SET {', '.join([f'{col} = %s' for col in labels])} WHERE ClassID = %s"
        elif table_name == "Teacher":
            query = f"UPDATE {table_name} SET {', '.join([f'{col} = %s' for col in labels])} WHERE TeacherID = %s"

        execute_query(query, values)
        load_data(table_name, tree)


def save_data(table_name, treeview):
    load_data(table_name, treeview)

def sort_data(table_name, treeview, sort_var, sort_column):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="1221",
            database="db"
        )
        cursor = connection.cursor()
        query = f"SELECT * FROM {table_name} ORDER BY {sort_column} {sort_var.get()}"
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()
        for i in treeview.get_children():
            treeview.delete(i)
        for row in data:
            treeview.insert("", "end", values=row)
    except mysql.connector.Error as err:
        print(f"Ошибка при сортировке данных: {err}")

def search_data(table_name, treeview, search_var, search_column):
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password="1221",
            database="db"
        )
        cursor = connection.cursor()
        query = f"SELECT * FROM {table_name} WHERE {search_column} LIKE %s"
        cursor.execute(query, (f"%{search_var.get()}%",))
        data = cursor.fetchall()
        connection.close()
        for i in treeview.get_children():
            treeview.delete(i)
        for row in data:
            treeview.insert("", "end", values=row)
    except mysql.connector.Error as err:
        print(f"Ошибка при поиске данных: {err}")

def generate_report(table_name, search_var, sort_var):
    search_criteria = search_var.get()
    sort_criteria = sort_var.get()
    report = f"Отчет\nПоиск: {search_criteria}\nСортировка: {sort_criteria}\n"
    treeview = None
    columns = []

    if table_name == "Class":
        report += "Таблица: Class\n\n"
        treeview = treeview1
        columns = ["ClassID", "Subject", "HoursPerWeek"]

    elif table_name == "ClassSubject":
        report += "Таблица: ClassSubject\n\n"
        treeview = treeview2
        columns = ["ClassID", "ClassLetter", "Subject", "TeacherID"]

    elif table_name == "Teacher":
        report += "Таблица: Teacher\n\n"
        treeview = treeview3
        columns = ["TeacherID", "TeacherName", "Specialization", "Experience"]

    report += "\t".join(columns) + "\n"

    for i in treeview.get_children():
        item = treeview.item(i)['values']
        report += "\t".join(map(str, item)) + "\n"

    report_window = tk.Toplevel(root)
    report_window.title("Отчет")

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

delete_button1 = tk.Button(tab1, text="Удалить", command=lambda: delete_data("Class", treeview1))
delete_button1.grid(row=len(labels_class) + 1, column=0, padx=10, pady=5)

edit_button1 = tk.Button(tab1, text="Изменить", command=lambda: edit_data("Class", treeview1, entry_var_class, labels_class))
edit_button1.grid(row=len(labels_class) + 1, column=1, padx=10, pady=5)

add_button1 = tk.Button(tab1, text="Добавить", command=lambda: add_data("Class", treeview1, entry_var_class, labels_class))
add_button1.grid(row=len(labels_class) + 2, column=0, padx=10, pady=5)

save_button1 = tk.Button(tab1, text="Сохранить", command=lambda: save_data("Class", treeview1))
save_button1.grid(row=len(labels_class) + 2, column=1, padx=10, pady=5)

search_var1 = tk.StringVar()
search_entry1 = tk.Entry(tab1, textvariable=search_var1)
search_entry1.grid(row=len(labels_class) + 3, column=0, padx=10, pady=5)
search_button1 = tk.Button(tab1, text="Поиск", command=lambda: search_data("Class", treeview1, search_var1, "Subject"))
search_button1.grid(row=len(labels_class) + 3, column=1, padx=10, pady=5)

sort_var1 = tk.StringVar()
sort_option1 = ttk.Combobox(tab1, textvariable=sort_var1, values=["ASC", "DESC"])
sort_option1.grid(row=len(labels_class) + 4, column=0, padx=10, pady=5)
sort_option1.set("ASC")
sort_button1 = tk.Button(tab1, text="Сортировка", command=lambda: sort_data("Class", treeview1, sort_var1, "Subject"))
sort_button1.grid(row=len(labels_class) + 4, column=1, padx=10, pady=5)

report_button1 = tk.Button(tab1, text="Генерировать отчет", command=lambda: generate_report("Class", search_var1, sort_var1))
report_button1.grid(row=len(labels_class) + 5, column=0, columnspan=2, padx=10, pady=5)

# Вкладка "ClassSubject"

delete_button2 = tk.Button(tab2, text="Удалить", command=lambda: delete_data("ClassSubject", treeview2))
delete_button2.grid(row=len(labels_class_subject) + 1, column=0, padx=10, pady=5)

edit_button2 = tk.Button(tab2, text="Изменить", command=lambda: edit_data("ClassSubject", treeview2, entry_var_class_subject, labels_class_subject))
edit_button2.grid(row=len(labels_class_subject) + 1, column=1, padx=10, pady=5)

add_button2 = tk.Button(tab2, text="Добавить", command=lambda: add_data("ClassSubject", treeview2, entry_var_class_subject, labels_class_subject))
add_button2.grid(row=len(labels_class_subject) + 2, column=0, padx=10, pady=5)

save_button2 = tk.Button(tab2, text="Сохранить", command=lambda: save_data("ClassSubject", treeview2))
save_button2.grid(row=len(labels_class_subject) + 2, column=1, padx=10, pady=5)

search_var2 = tk.StringVar()
search_entry2 = tk.Entry(tab2, textvariable=search_var2)
search_entry2.grid(row=len(labels_class_subject) + 3, column=0, padx=10, pady=5)
search_button2 = tk.Button(tab2, text="Поиск", command=lambda: search_data("ClassSubject", treeview2, search_var2, "Subject"))
search_button2.grid(row=len(labels_class_subject) + 3, column=1, padx=10, pady=5)

sort_var2 = tk.StringVar()
sort_option2 = ttk.Combobox(tab2, textvariable=sort_var2, values=["ASC", "DESC"])
sort_option2.grid(row=len(labels_class_subject) + 4, column=0, padx=10, pady=5)
sort_option2.set("ASC")
sort_button2 = tk.Button(tab2, text="Сортировка", command=lambda: sort_data("ClassSubject", treeview2, sort_var2, "Subject"))
sort_button2.grid(row=len(labels_class_subject) + 4, column=1, padx=10, pady=5)

report_button2 = tk.Button(tab2, text="Генерировать отчет", command=lambda: generate_report("ClassSubject", search_var2, sort_var2))
report_button2.grid(row=len(labels_class_subject) + 5, column=0, columnspan=2, padx=10, pady=5)

# Вкладка "Teacher"

delete_button3 = tk.Button(tab3, text="Удалить", command=lambda: delete_data("Teacher", treeview3))
delete_button3.grid(row=len(labels_teacher) + 1, column=0, padx=10, pady=5)

edit_button3 = tk.Button(tab3, text="Изменить", command=lambda: edit_data("Teacher", treeview3, entry_var_teacher, labels_teacher))
edit_button3.grid(row=len(labels_teacher) + 1, column=1, padx=10, pady=5)

add_button3 = tk.Button(tab3, text="Добавить", command=lambda: add_data("Teacher", treeview3, entry_var_teacher, labels_teacher))
add_button3.grid(row=len(labels_teacher) + 2, column=0, padx=10, pady=5)

save_button3 = tk.Button(tab3, text="Сохранить", command=lambda: save_data("Teacher", treeview3))
save_button3.grid(row=len(labels_teacher) + 2, column=1, padx=10, pady=5)

search_var3 = tk.StringVar()
search_entry3 = tk.Entry(tab3, textvariable=search_var3)
search_entry3.grid(row=len(labels_teacher) + 3, column=0, padx=10, pady=5)
search_button3 = tk.Button(tab3, text="Поиск", command=lambda: search_data("Teacher", treeview3, search_var3, "TeacherName"))
search_button3.grid(row=len(labels_teacher) + 3, column=1, padx=10, pady=5)

sort_var3 = tk.StringVar()
sort_option3 = ttk.Combobox(tab3, textvariable=sort_var3, values=["ASC", "DESC"])
sort_option3.grid(row=len(labels_teacher) + 4, column=0, padx=10, pady=5)
sort_option3.set("ASC")
sort_button3 = tk.Button(tab3, text="Сортировка", command=lambda: sort_data("Teacher", treeview3, sort_var3, "TeacherName"))
sort_button3.grid(row=len(labels_teacher) + 4, column=1, padx=10, pady=5)

report_button3 = tk.Button(tab3, text="Генерировать отчет", command=lambda: generate_report("Teacher", search_var3, sort_var3))
report_button3.grid(row=len(labels_teacher) + 5, column=0, columnspan=2, padx=10, pady=5)

root.mainloop()
