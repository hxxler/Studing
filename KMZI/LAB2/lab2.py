import tkinter as tk
import hashlib
import matplotlib.pyplot as plt
import random

# Функция для вычисления хэш-функции SHA-384
def calculate_sha384_hash(text):
    sha384_hash = hashlib.sha384(text.encode()).hexdigest()
    return sha384_hash

# Функция для исследования лавинного эффекта и построения графика
def analyze_avalanche_effect(text, rounds):
    original_hash = calculate_sha384_hash(text)
    changed_hashes = []
    
    for round in range(rounds):
        position = random.randint(0, len(text) - 1)  # Выбираем случайную позицию для изменения бита
        text = change_bit(text, position)
        changed_hash = calculate_sha384_hash(text)
        changed_bits = sum(1 for a, b in zip(original_hash, changed_hash) if a != b)
        changed_hashes.append(changed_bits)
    
    plt.plot(range(rounds), changed_hashes)
    plt.xlabel('Раунды')
    plt.ylabel('Измененные биты в хэше')
    plt.title('Зависимость числа измененных бит от раунда')
    plt.grid(True)
    plt.show()

# Функция для изменения бита в тексте
def change_bit(text, position):
    text_list = list(text)
    text_list[position] = '1' if text_list[position] == '0' else '0'
    return ''.join(text_list)

# Создание графического интерфейса с использованием Tkinter
root = tk.Tk()
root.title('SHA-384 Hash and Avalanche Effect Analyzer')

# Фрейм для текстового ввода и меток
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Поле для ввода текста сообщения
text_label = tk.Label(input_frame, text='Текст сообщения:')
text_label.pack(side='left', padx=5)
text_entry = tk.Entry(input_frame, width=40)
text_entry.pack(side='left')

# Фрейм для кнопок
button_frame = tk.Frame(root)
button_frame.pack()

# Функция для вычисления и отображения хэш-функции
def calculate_and_display_hash():
    input_text = text_entry.get()
    if input_text:
        hash_result = calculate_sha384_hash(input_text)
        hash_output.config(text=f'SHA-384 хэш: {hash_result}')

hash_button = tk.Button(button_frame, text='Вычислить SHA-384 хэш', command=calculate_and_display_hash)
hash_button.pack(side='left', padx=5)

# Поле для вывода хеш-функции
hash_output = tk.Label(root, text='', wraplength=400)
hash_output.pack()

# Функция для анализа лавинного эффекта
def analyze_effect():
    input_text = text_entry.get()
    rounds = 30  # Количество раундов для анализа
    analyze_avalanche_effect(input_text, rounds)

analyze_button = tk.Button(button_frame, text='Анализировать лавинный эффект', command=analyze_effect)
analyze_button.pack(side='left', padx=5)

root.mainloop()
