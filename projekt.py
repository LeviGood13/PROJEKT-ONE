import tkinter as tk
from tkinter import ttk
import sqlite3
# Класс Главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    # иницициализация виджетов главного окна
    def init_main(self):
        # Верхняя панель для кнопок
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        #Создание картинки
        self.add_img = tk.PhotoImage(file='./img/add.png')
        #Создание кнопки
        #bd - граница
        btn_open_dialog = tk.Button(toolbar, bg='#d7d7d7', bd=0, image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)


        # Кнопка редактирования
        self.upd_img = tk.PhotoImage(file='./img/update.png')
        btn_upd_dialog = tk.Button(toolbar, bg='#d7d7d7', bd=0, image=self.upd_img, command=self.open_update_dialog)
        btn_upd_dialog.pack(side=tk.LEFT)

        # Кнопка удаления записей
        self.del_img = tk.PhotoImage(file='./img/delete.png')
        btn_del_dialog = tk.Button(toolbar, bg='#d7d7d7', bd=0, image=self.del_img, command=self.delete_record)
        btn_del_dialog.pack(side=tk.LEFT)

        # Кнопка поиска
        self.search_img = tk.PhotoImage(file='./img/search.png')
        btn_search_dialog = tk.Button(toolbar, bg='#d7d7d7', bd=0, image=self.search_img, command=self.open_search_dialog)
        btn_search_dialog.pack(side=tk.LEFT)

        # кнопка обновления таблицы
        self.refresh_img = tk.PhotoImage(file='./img/refresh.png')
        btn_refresh_dialog = tk.Button(toolbar, bg='#d7d7d7', bd=0, image=self.refresh_img, command=self.view_records)
        btn_refresh_dialog.pack(side=tk.LEFT)

        # Создание Treeview (таблицы контактов)
        # columns - столбцы
        # height - высота таблицы
        # show='headings' скрываем нулевой текст
        self.tree=ttk.Treeview(self, columns=['ID', 'name', 'phone', 'email', 'salary'], height=45, show='headings')
        #задаем ширину и выравнивание текста
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=260, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=100, anchor=tk.CENTER)

        #задаем подписи столбцам
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('phone', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')
        self.tree.pack(side=tk.LEFT)

        # скроллбар
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # метод для вызова добавления новых данных
    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    # изменение данных (строки) в БД
    def update_record(self, name, phone, email, salary):
        self.db.c.execute('''
        UPDATE employes 
        SET name = ?, phone = ?, email = ?, salary = ?
        WHERE id = ? ''', (name, phone, email, salary, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

    # удаление данных (выделенной строки из БД)
    def delete_record(self):
        for sel_row in self.tree.selection():
            self.db.c.execute('''
            DELETE FROM employes
            WHERE id=?
            ''', (self.tree.set(sel_row, '#1'), ))
        self.db.conn.commit()
        self.view_records()

    # Метод поиска записей по ФИО
    def search_records(self, name):
        self.db.c.execute('''
        SELECT * 
        FROM employes
        WHERE name LIKE ?''', ('%'+ name +'%',))
        r = self.db.c.fetchall()
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in r]


    # метод отображения данных
    def view_records(self):
        self.db.c.execute(''' SELECT * FROM employes''')
        r = self.db.c.fetchall()
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=i) for i in r]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()

# Класс дочерних окон
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # иницициализация виджетов главного окна
    def init_child(self):
        self.title('Добавление сотрудника')
        self.geometry('400x200')
        self.resizable(False, False)
        #перехватываем все события
        self.grab_set()
        #захватываем фокус
        self.focus_set()

        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=20)
        label_phone = tk.Label(self, text='Телефон:')
        label_phone.place(x=50, y=50)
        label_email = tk.Label(self, text='E-mail:')
        label_email.place(x=50, y=80)
        label_salary = tk.Label(self, text='Зарплата')
        label_salary.place(x=50, y=110)

        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=150,y=20)

        self.entry_phone = tk.Entry(self)
        self.entry_phone.place(x=150,y=50)

        self.entry_email = tk.Entry(self)
        self.entry_email.place(x=150,y=80)

        self.entry_salary = tk.Entry(self)
        self.entry_salary.place(x=150,y=110)
        
        # кнопка закрытия
        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=218, y=140)
        
        # кнопка добавить
        self.btn_ok = tk.Button(self, text='Добавить')
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.records( self.entry_name.get(), self.entry_phone.get(), self.entry_email.get(), self.entry_salary.get()))
        self.btn_ok.place(x=150, y=140)

# Класс для обновления (изменения) данных (наследуется от Child)
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.db = db
        self.load_data()

    # инициализация виджетов окна редактирования данных
    def init_edit(self):
        self.title('Редактирование контакта')
        btn_edit = tk.Button(self, text='Изменить')
        btn_edit.bind('<Button-1>', lambda ev: self.view.update_record(self.entry_name.get(), self.entry_phone.get(), self.entry_email.get(), self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        btn_edit.place(x=150, y=140)
        self.btn_ok.destroy()

    # Подстановка данных (старых)
    def load_data(self):
        self.db.c.execute('''
        SELECT * 
        FROM employes
        WHERE id = ?
        ''', self.view.tree.set(self.view.tree.selection()[0], '#1'))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

# класс дочерего окна для поиска по ФИО     
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # иницициализация виджетов главного окна для поиска
    def init_child(self):
        self.title('Поиск')
        self.geometry('400x200')
        self.resizable(False, False)
        #перехватываем все события
        self.grab_set()
        #захватываем фокус
        self.focus_set()

        label_name = tk.Label(self, text='ФИО:')
        label_name.place(x=50, y=80)
        
        self.entry_name = tk.Entry(self)
        self.entry_name.place(x=150,y=80)

        # кнопка закрытия
        self.btn_cancel = tk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=218, y=140)
        
        # кнопка поиска
        self.btn_ok = tk.Button(self, text='Найти')
        self.btn_ok.bind('<Button-1>', lambda ev: self.view.search_records(self.entry_name.get()))
        self.btn_ok.bind('<Button-1>', lambda ev: self.destroy(), add='+')
        self.btn_ok.place(x=150, y=140)

# класс БД
class Db:
    def __init__(self):
        self.conn = sqlite3.connect('employes.db')
        self.c = self.conn.cursor()
        self.c.execute('''
                          CREATE TABLE IF NOT EXISTS employes (
                       id INTEGER PRIMARY KEY,
                       name TEXT,
                       phone TEXT,
                       email TEXT,
                       salary TEXT)
                       ''')
        self.conn.commit()

        # Добавление в бд
    def insert_data(self, name, phone, email, salary):
         self.c.execute('''
                INSERT INTO employes (name, phone, email, salary)
                VALUES (?, ?, ?, ?)
                ''', (name, phone, email, salary))
         self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    db = Db()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('710x450+300+200')
    root.resizable(False, False)
    root.mainloop()