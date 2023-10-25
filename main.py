import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):   # отвечает за главное окно, хранение, инициализация
    def __init__(self,root):
        super().__init__(root)
        self.init_main()
        self.db=db
        self.view_records()

    def init_main(self):                     #метод с графическими вещами
        toolbar=tk.Frame(bg='#d7d8e0',bd=2)  #кнопка для добавления
        toolbar.pack(side=tk.TOP, fill=tk.X)
       # self.add_img= tk.PhotoImage(file='./img/add.png')
        btn_open_dialog=tk.Button(toolbar, text= 'Добавить',bd=0, command=self.open_dialog)  # кнопка добавления
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree=ttk.Treeview(self,columns=('id', 'ФИО', 'email','телефон','зарплата'), height=45,show='headings') #главная таблицы

        self.tree.column('id',width=30, anchor=tk.CENTER)     # параметры столбцов главной таблицы
        self.tree.column ('ФИО', width=300, anchor=tk.CENTER)
        self.tree.column ('телефон', width=150, anchor=tk.CENTER)
        self.tree.column ('email', width=150, anchor=tk.CENTER)
        self.tree.column ('зарплата', width=150, anchor=tk.CENTER)

        self.tree.heading('id',text='ID')     # названия столбцов таблицы
        self.tree.heading('ФИО',text='ФИО')
        self.tree.heading('телефон',text='телефон')
        self.tree.heading('email',text='email')
        self.tree.heading('зарплата',text='зарплата')

        self.tree.pack(side=tk.LEFT)

        button_update_dialog = tk.Button (toolbar, text='Редактировать', bd=0, command=self.open_update_dialog)  # кнопка update
        button_update_dialog.pack (side=tk.LEFT)

        button_delete= tk.Button(toolbar, text='Удалить', bd=0, command=self.delete_records)
        button_delete.pack (side=tk.LEFT)

        btn_search=tk.Button(toolbar, text='Поиск', bd=0, command=self.open_search_dialog)
        btn_search.pack (side=tk.LEFT)

        btn_search = tk.Button (toolbar, text='Обновить', bd=0, command=self.update_tabl)
        btn_search.pack (side=tk.LEFT)

    # def open_dialog(self):
    #     Child(self)          # метод для вызова дочернего окна 16стр
    def open_dialog(self):
        child_window = Child (self)  # Create an instance of Child
        child_window.open ()

    def update_tabl(self):
        self.view_records()

    def records(self, name, tel,email, zp):    # добавление новых данных в бд из окна
        self.db.insert_data( name, tel, email, zp)
        self.view_records ()
    def view_records(self):    #вывод двнных всех данных на главное окно(обновление)
        self.db.cursor.execute('SELECT * FROM db')
        [self.tree.delete(i) for i in self.tree.get_children()] #для очистки записаной информации
        [self.tree.insert('','end',values= row) for row in self.db.cursor.fetchall()] #добавить в виджет таблицм всю информацию

    # def open_update_dialog(self):
    #     UpDate (self)
    def open_update_dialog(self):
        try:
            selected_item = self.tree.selection ()[0]
            update_window = UpDate (self)
            update_window.open ()
            update_window.default_data (selected_item)
        except IndexError:
            # # Показывать всплывающее окно с ошибкой, если ни один элемент не выбран
            self.show_error_popup ("Выберите контакт для редактирования")

    def show_error_popup(self, message):
        error_popup = tk.Toplevel ()
        error_popup.title ("Error")
        error_popup.geometry ("300x100")
        label = tk.Label (error_popup, text=message, wraplength=250)
        label.pack (padx=20, pady=20)
        ok_button = tk.Button (error_popup, text="OK", command=error_popup.destroy)
        ok_button.pack (pady=10)
        error_popup.focus_set ()
        error_popup.grab_set ()
    def update_records(self, name,tel,email,zp):
        self.db.cursor.execute('''UPDATE db SET name=?, tel=?, email=?, zp=? WHERE id=?''', (name,tel,email,zp, self.tree.set(self.tree.selection()[0],'#1'))) #берем 1 выдел строку и берем значение 1 столбца и изменяем данные
        self.db.conn.commit()
        self.view_records()

    # def delete_records(self):
    #     for selection_item in self.tree.selection ():
    #         item = self.tree.item (selection_item)
    #         item_id = item['values'][0]  # The ID is the first value in the row
    #         self.db.cursor.execute ('DELETE FROM db WHERE id=?', (item_id,))
    #     self.db.conn.commit ()
    #     self.view_records ()

    def delete_records(self):
        selected_item = self.tree.selection ()
        if not selected_item:
            # Если строка не выбрана, отобразите сообщение и верните
            self.show_message ("Не выбрана строка. Пожалуйста, выберите строку перед удалением.")
            return

        for selection_item in selected_item:
            item = self.tree.item (selection_item)
            item_id = item['values'][0]  # Идентификатор - это первое значение в строке
            self.db.cursor.execute ('DELETE FROM db WHERE id=?', (item_id,))
        self.db.conn.commit ()
        self.view_records ()

    def show_message(self, message):
        message_window = tk.Toplevel (self)
        message_window.title ("Message")
        message_label = tk.Label (message_window, text=message)
        message_label.pack ()
        close_button = tk.Button (message_window, text="OK", command=message_window.destroy)
        close_button.pack ()

    def open_search_dialog(self):
        Search(self)

    def search_records(self, name):
        name = '%' + name + '%'
        name = name.lower ()  # Преобразуйте поисковый запрос в нижний регистр

        self.db.cursor.execute ('SELECT * FROM db WHERE LOWER(name) LIKE ?', (name,))
        filtered_contacts = self.db.cursor.fetchall ()

        # Clear previous search results
        [self.tree.delete (i) for i in self.tree.get_children ()]

        # Define a tag configuration
        self.tree.tag_configure ('found', background='yellow', foreground='black')  #  Измените эти цвета по мере необходимости


        for row in filtered_contacts:
            item_id = row[0]
            values = row[0:]
            self.tree.insert ('', 'end', values=values, tags=('found',))
            self.tree.tag_bind ('found', '<Button-1>',
                                lambda event, item_id=item_id: self.show_contact_details (item_id))

        if not filtered_contacts:
            self.view_records ()  #  Если результат поиска пуст, отобразите все контакты.


# class Child(tk.Toplevel):
#     def __init__(self, app):    # инициализация диалогового окна
#         super().__init__(root)
#         self.init_child()
#         self.view = app
class Child (tk.Toplevel):
    def __init__(self, app):
        super ().__init__ (root)
        self.init_child ()
        self.view = app
        self.withdraw ()

    def open(self):
        self.deiconify ()

    def init_child(self):       # графич характеристики внутри дочернего окна
        self.title('Добавить')
        self.geometry('400x320')
        self.resizable(False,False)

        self.grab_set()
        self.focus_set()

        label_name= tk.Label(self,text='ФИО:')    # строки добавления данных
        label_name.place(x=50,y=50)
        label_select=tk.Label(self,text='телефон:')
        label_select.place(x=50,y=80)
        label_email=tk.Label (self, text='email:')
        label_email.place (x=50, y=110)
        label_zp=tk.Label(self,text='зарплата:')
        label_zp.place(x=50,y=145)

        self.entry_name=ttk.Entry(self)    # разметка строк добавления
        self.entry_name.place(x=200,y=50)
        self.entry_tel = ttk.Entry (self)
        self.entry_tel.place (x=200, y=80)
        self.entry_email = ttk.Entry (self)
        self.entry_email.place (x=200, y=110)
        self.entry_zp = ttk.Entry (self)
        self.entry_zp.place (x=200, y=145)

        self.btn_cancel=ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=200)   # кнопка для закрытия окна

        self.btn_ok=ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=200)       # кнопка на добавление

        self.btn_ok.bind('<Button-1>', lambda even:           # обрабатываем щелчок мышки по кнопкам и передаем в метод рекордс наши параметры с помощью get
                         self.view.records(self.entry_name.get(),
                                           self.entry_email.get(),
                                           self.entry_tel.get(),
                                           self.entry_zp.get()))




class UpDate(Child):
    def __init__(self, app):
        super().__init__(app)
        self.init_edit()
        self.view = app
        self.db = db
        self.withdraw()  # Hide the window initially
        self.default_data()

    def open(self):
        self.deiconify()

    def init_edit(self):
        self.title('Редактировать контакт')
        btn_edit=ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=200)
        btn_edit.bind('<Button-1>', lambda evennt:
                      self.view.update_records(self.entry_name.get(),  # отправляет данные в бд при нажатии на кнопку
                                               self.entry_email.get(),
                                               self.entry_tel.get(),
                                               self.entry_zp.get()))
        btn_edit.bind('<Button-1>',lambda event: self.destroy(), add='+') # закрывает окно при нажатии на кнопку
        self.btn_ok.destroy()

    def default_data(self):  # добавление данных из табл при редактировании
        self.db.cursor.execute ('SELECT * FROM db WHERE id=?',
                                (self.view.tree.set (self.view.tree.selection ()[0], '#1'),))

        row = self.db.cursor.fetchall ()
        self.entry_name.insert (0, row[0][1])
        self.entry_email.insert (0, row[0][2])
        self.entry_tel.insert (0, row[0][3])
        self.entry_zp.insert (0, row[0][4])

    # def default_data(self):
    #     item_id = self.view.tree.selection ()[0]
    #     self.db.cursor.execute ('SELECT * FROM db WHERE id=?', (item_id,))
    #     result = self.db.cursor.fetchall ()
    #     if result:
    #         row = self.db.cursor.fetchall ()
    #         self.entry_name.insert (0, row[0][1])
    #         self.entry_email.insert (0, row[0][2])
    #         self.entry_tel.insert (0, row[0][3])
    #         self.entry_zp.insert (0, row[0][4])


class Search(tk.Toplevel):
    def __init__(self,app):
        super().__init__(app)
        self.init_search()
        self.view=app

    def init_search(self):
        self.title('Поиск контакта')
        self.geometry('300x100')
        self.resizable(False,False)

        label_search=tk.Label(self, text='Имя: ')
        label_search.place(x=50,y=20)

        self.entry_search=ttk.Entry(self)
        self.entry_search.place(x=100, y=20, width=150)

        btn_cancel = ttk.Button (self, text='Закрыть', command=self.destroy )

        btn_cancel.place(x=185, y=50)

        btn_search=ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event:
                        self.view.search_records(self.entry_search.get()))
        btn_search.bind ('<Button-1>', lambda event: self.destroy(), add='+')

class DB:
    def __init__(self):
        self.conn=sqlite3.connect('db.db') # инициализируем бд создаем файл
        self.cursor= self.conn.cursor()    # подключаем объект курсор
        self.cursor.execute(               # запрос на создание таблицы
            '''CREATE TABLE IF NOT EXISTS db (
                id INTEGER PRIMARY KEY,
                name TEXT,
                tel TEXT,
                email TEXT,
                zp TEXT)'''
        )
        self.conn.commit()        # сохраняем

    def insert_data(self,name,tel, email, zp):  # метод для добавления данных в таблицу
        self.cursor.execute(     # запрос на добавление
            '''INSERT INTO db(name,tel, email, zp) VALUES (?,?,?,?)''', (name,tel,email,zp)
        )
        self.conn.commit()       # сохраняем


if __name__ == '__main__':        # это база
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('телефонная книга')
    root.geometry('778x450')
    root.resizable(False, False)
    root.mainloop()
