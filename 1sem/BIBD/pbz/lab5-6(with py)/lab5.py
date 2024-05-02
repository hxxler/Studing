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
        values = [tree.item(selected_item)['values'][0]]
        if table_name == "Class":
            query = f"DELETE FROM {table_name} WHERE ClassID = %s"
        elif table_name == "ClassSubject":
            query = f"DELETE FROM {table_name} WHERE ClassID = %s"
        elif table_name == "Teacher":
            query = f"DELETE FROM {table_name} WHERE TeacherID = %s"
        execute_query(query, values)
        load_data(table_name, tree)


def edit_data(table_name, tree, entry_vars, labels):
    selected_item = tree.selection()
    if selected_item:
        values = [entry_vars[i].get() for i in range(len(entry_vars))]
        values.append(tree.item(selected_item)['values'][0])
        query = f"UPDATE {table_name} SET {', '.join([f'{col} = %s' for col in labels])} WHERE {table_name}ID = %s"
        execute_query(query, values)
        load_data(table_name, tree)

def add_data(table_name, tree, entry_vars, labels):
    values = [entry_vars[i].get() for i in range(len(entry_vars))]
    query = f"INSERT INTO {table_name} ({', '.join(labels)}) VALUES ({', '.join(['%s' for _ in range(len(entry_vars))])})"
    execute_query(query, values)
    load_data(table_name, tree)

def save_data(table_name, treeview):
    load_data(table_name, treeview)

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

delete_button2 = tk.Button(tab2, text="Удалить", command=lambda: delete_data("ClassSubject", treeview2))
delete_button2.grid(row=len(labels_class_subject) + 1, column=0, padx=10, pady=5)

edit_button2 = tk.Button(tab2, text="Изменить", command=lambda: edit_data("ClassSubject", treeview2, entry_var_class_subject, labels_class_subject))
edit_button2.grid(row=len(labels_class_subject) + 1, column=1, padx=10, pady=5)

add_button2 = tk.Button(tab2, text="Добавить", command=lambda: add_data("ClassSubject", treeview2, entry_var_class_subject, labels_class_subject))
add_button2.grid(row=len(labels_class_subject) + 2, column=0, padx=10, pady=5)

save_button2 = tk.Button(tab2, text="Сохранить", command=lambda: save_data("ClassSubject", treeview2))
save_button2.grid(row=len(labels_class_subject) + 2, column=1, padx=10, pady=5)

delete_button3 = tk.Button(tab3, text="Удалить", command=lambda: delete_data("Teacher", treeview3))
delete_button3.grid(row=len(labels_teacher) + 1, column=0, padx=10, pady=5)

edit_button3 = tk.Button(tab3, text="Изменить", command=lambda: edit_data("Teacher", treeview3, entry_var_teacher, labels_teacher))
edit_button3.grid(row=len(labels_teacher) + 1, column=1, padx=10, pady=5)

add_button3 = tk.Button(tab3, text="Добавить", command=lambda: add_data("Teacher", treeview3, entry_var_teacher, labels_teacher))
add_button3.grid(row=len(labels_teacher) + 2, column=0, padx=10, pady=5)

save_button3 = tk.Button(tab3, text="Сохранить", command=lambda: save_data("Teacher", treeview3))
save_button3.grid(row=len(labels_teacher) + 2, column=1, padx=10, pady=5)

root.mainloop()
