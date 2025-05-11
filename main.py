import tkinter as tk
from tkinter import *
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox
import json
import os
from datetime import datetime

home_dir = os.path.expanduser('~')
tasks_file_path = os.path.join(home_dir, 'tasks.json')
data = {'tasks': []}
DATA_FILE = 'data.json'

root = tk.Tk()

root.title('MyListTo-Do')
root.configure(background='beige')
root.minsize(250, 250)
root.maxsize(450, 500)

tk.Label(root, text='Мой список дел', bg='beige', font=('Arial', 16)).pack(pady=10)

listbox = tk.Listbox(root, height=10, width=40)
listbox.pack(pady=30)

entry = tk.Entry(root, font=('Arial', 8))
entry.pack()

entry_deadline = tk.Entry(root, font=('Arial', 8))
entry_deadline.pack()

current_edit_index = None
all_tasks = [] 

def get_all_tasks():
    return list(all_tasks)


def update_listbox_from_all_tasks():
    listbox.delete(0, 'end')
    for task in all_tasks:
        text = task['text']
        deadline = f' (до {task['deadline']})' if task['deadline'] else ''
        display_text = text + deadline

        bg_color = 'white'
        if task['is_done']:
            display_text = u'\u2713 ' + display_text
            bg_color = 'lightgreen'
        elif task['is_important']:
            display_text = '!' + display_text
            bg_color = 'orange'
        
        if task['deadline']:
            deadline_date = datetime.strptime(task['deadline'], '%d.%m.%Y')
            if deadline_date < datetime.now():
                bg_color = 'red'

        listbox.insert('end', display_text)
        index = listbox.size() - 1
        listbox.itemconfig(index, {'bg': bg_color})


def add_to_listbox():
    task_text = entry.get()
    deadline_user_input = entry_deadline.get()
    if task_text:
        new_task = {
            'text': task_text,
            'is_done': False,
            'is_important': False,
            'deadline': deadline_user_input if deadline_user_input else None
        }
        all_tasks.append(new_task)
        update_listbox_from_all_tasks()
        auto_save()
        entry.delete(0, 'end')
        entry_deadline.delete(0, 'end')


def remove_task():
    selected = listbox.curselection()
    if not selected:
        return
    i = selected[0]
    del all_tasks[i]
    update_listbox_from_all_tasks()


def auto_save():
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(all_tasks, f, indent=4)
    except Exception as e:
        print(f'Ошибка при сохранении: {e}')


def save_task_as_file():
    if not all_tasks:
        messagebox.showinfo('Пусто', 'Список задач пуст.')
        return
    files = [('Text file', '*.txt'), ('JSON file', '*.json'), ('All files', '*.*')]
    file = asksaveasfile(mode='w', filetypes=files, defaultextension=files)
    if file:
        try:
            json.dump(all_tasks, file, indent=4)
            file.close()
        except Exception as e:
            messagebox.showerror('Ошибка', f'Не удалось сохранить файл:\n{e}')


def auto_load_tasks():
    global all_tasks
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as f:
                loaded = json.load(f)
                print('Загруженные данные:', loaded)
                if isinstance(loaded, list):
                    all_tasks.clear()
                    all_tasks.extend(loaded)
                    print('Задачи успешно загружены.')
                else:
                    print('Формат данных не список.')
        except Exception as e:
            print(f'Ошибка при загрузке: {e}')


def on_closing():
    auto_save()
    root.destroy()


def edit_task():
    global current_edit_index
    selected = listbox.curselection()
    if not selected:
        return
    current_edit_index = selected[0]
    task = all_tasks[current_edit_index]
    entry.delete(0, 'end')
    entry.insert(0, task['text'])
    entry_deadline.delete(0, 'end')
    entry_deadline.insert(0, task['deadline'] if task['deadline'] else '')


def save_edit_task():
    global current_edit_index
    if current_edit_index is not None:
        new_text = entry.get().strip()
        new_deadline = entry_deadline.get().strip()
        if new_text:
            task = all_tasks[current_edit_index]
            task['text'] = new_text
            task['deadline'] = new_deadline if new_deadline else None
            update_listbox_from_all_tasks()
        entry.delete(0, 'end')
        entry_deadline.delete(0, 'end')
        current_edit_index = None


def toggle_as_done():
    index = listbox.curselection()
    if not index:
        return
    i = index[0]
    task = all_tasks[i]
    task['is_done'] = not task['is_done']
    update_listbox_from_all_tasks()


def toggle_as_important():
    index = listbox.curselection()
    if not index:
        return
    i = index[0]
    task = all_tasks[i]
    task['is_important'] = not task['is_important']
    update_listbox_from_all_tasks()


def show_all_tasks():
    update_listbox_from_all_tasks()


def show_only_done():
    listbox.delete(0, 'end')
    for task in all_tasks:
        if task['is_done']:
            text = task['text']
            deadline = f' (до {task['deadline']})' if task['deadline'] else ''
            listbox.insert('end', u'\u2713 ' + text + deadline)
            index = listbox.size() - 1
            listbox.itemconfig(index, {'bg': 'lightgreen'})


def show_only_important():
    listbox.delete(0, 'end')
    for task in all_tasks:
        if task['is_important']:
            text = task['text']
            deadline = f' (до {task['deadline']})' if task['deadline'] else ''
            listbox.insert('end', '!' + text + deadline)
            index = listbox.size() - 1
            listbox.itemconfig(index, {'bg': 'orange'})

# Фреймы
button_frame1 = tk.Frame(root, bg='beige')
button_frame1.pack(pady=5)

button_frame2 = tk.Frame(root, bg='beige')
button_frame2.pack(pady=5)

button_frame3 = tk.Frame(root, bg='beige')
button_frame3.pack(pady=5)

button_frame4 = tk.Frame(root, bg='beige')
button_frame4.pack(pady=5)

button_frame5 = tk.Frame(root, bg='beige')
button_frame5.pack(pady=5)

# Кнопки
tk.Button(button_frame1, text='Добавить', command=add_to_listbox).pack(side='left', padx=5)
tk.Button(button_frame1, text='Удалить', command=remove_task).pack(side='left', padx=5)

tk.Button(button_frame2, text='Редактировать задачу', command=edit_task).pack(side='left', padx=5)
tk.Button(button_frame2, text='Сохранить задачу', command=save_edit_task).pack(side='left', padx=5)

tk.Button(button_frame3, text='Выполнено', command=toggle_as_done).pack(side='left', padx=5)
tk.Button(button_frame3, text='Важное', command=toggle_as_important).pack(side='left', padx=5)

tk.Button(button_frame4, text='Показать все', command=show_all_tasks).pack(side='left', padx=5)
tk.Button(button_frame4, text='Показать только важные', command=show_only_important).pack(side='left', padx=5)
tk.Button(button_frame4, text='Показать только выполненные', command=show_only_done).pack(side='left', padx=5)

tk.Button(button_frame5, text='Сохранить как файл', command=save_task_as_file).pack(side='left', padx=5)

auto_load_tasks()

root.protocol('WM_DELETE_WINDOW', on_closing)

root.mainloop()