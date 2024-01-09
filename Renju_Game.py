import tkinter as tk
from tkinter import ttk, messagebox as mb
from idlelib.tooltip import Hovertip
import random
import os

class WindowCreate(tk.Tk):
    def __init__(self):
        super().__init__()
        self.initialize_window()
    def initialize_window(self):# параметры главного окна
        self.geometry(f'{1005}x{730}+{250}+{12}')  # Размеры и положение окна
        self.resizable(False, False)  # Запрещаем изменение размеров окна
        self.title("Вход/Регистрация")  # Заголовок окна
        self.canvas = tk.Canvas(width=1209, height=810)# основной холст для размещения элементов
        self.canvas.place(relx=0.61, rely=0.55, anchor=tk.CENTER)
        self.canvas_mini = tk.Canvas(width=550, height=560, bg='#1B493F')# дополнительный холст с фоном
        self.canvas_mini.place(relx=0.5, rely=0.48, anchor=tk.CENTER)
        self.style = ttk.Style()# стиль для виджетов
        self.style.configure('TLabel', font=('Bahnschrift', 18), padding=10)
        self.style.configure('Btt.TButton', font=('Bahnschrift bold', 14), width=25, padding=7)
        self.boardIm = tk.PhotoImage(file="derevo2.png")# изображение для фона основного холста
        self.background_image = self.canvas.create_image(495, 358, anchor=tk.CENTER, image=self.boardIm)
class LoginWindow(WindowCreate):
    def __init__(self):# виджеты интерфейса для окна входа
        super().__init__()
        self.testL1 = tk.Label(text='ВХОД', bg='#1B493F', fg="white", font='Bahnschrift 24').place(relx=0.5, rely=0.2, anchor=tk.CENTER)
        self.testL2 = tk.Label(text='для подсказки наведите курсор на поле ввода', font=('Bahnschrift 14'), bg='#1B493F', fg="white").place(relx=0.5, rely=0.25, anchor=tk.CENTER)
        self.login_label = tk.Label(text="Логин:", bg='#1B493F', fg="white", font='Bahnschrift 24', width=12).place(relx=0.36, rely=0.4, anchor=tk.CENTER)
        self.login_entry = ttk.Entry(validate='key', validatecommand=(self.validate_length, "%P"), font='Bahnschrift 18', width=12)
        self.login_entry.place(relx=0.5, rely=0.4, anchor=tk.CENTER)
        self.password_label = tk.Label(text="Пароль:", bg='#1B493F', fg="white", font='Bahnschrift 24', width=12)
        self.password_label.place(relx=0.35, rely=0.5, anchor=tk.CENTER)
        self.password_entry = ttk.Entry(show='*', validate='key', validatecommand=(self.validate_length, "%P"), font='Bahnschrift 18', width=12)
        self.password_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.toggle_password_button = ttk.Button(text='Показать пароль', cursor='hand2', command=self.show_password)
        self.toggle_password_button.place(relx=0.65, rely=0.5, anchor=tk.CENTER)
        self.login_button = ttk.Button(text="Вход", command=self.login, cursor='hand2', style='Btt.TButton')
        self.login_button.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
        self.register_button = ttk.Button(width=25, text="Зарегистрироваться", command=self.add_user, cursor='hand2', style='Btt.TButton')
        self.register_button.place(relx=0.5, rely=0.75, anchor=tk.CENTER)
        self.TipLogin = Hovertip(self.login_entry, 'Логин должен быть более 5 символов \n и содержать хотя бы одну цифру, \n макс. длина - 10 символов') # всплывающие подсказки
        self.TipPassword = Hovertip(self.password_entry, 'Пароль должен быть более 7 символов \n и содержать хотя бы одну цифру и одну букву, \n макс. длина - 10 символов')
        if not os.path.exists('DataFile.json'):# Проверяем наличие файла данных, если нет - создаем
            with open('DataFile.json', 'w'):  pass
    def login(self):# Обработка события входа
        login = self.login_entry.get()
        password = self.password_entry.get()
        if not login or not password:
            mb.showerror("Авторизация", "Пожалуйста, заполните все поля")
            return
        with open("DataFile.json", "r") as file:
            lines = file.readlines()
            user_found = False
            incorrect_password = False
            for line in lines:
                stored_username, stored_password = line.strip().split('•')
                if login == stored_username:
                    if password == stored_password:
                        user_found = True
                        mb.showinfo("Авторизация", f"Добро пожаловать, {login}!")
                        self.show_game_window()
                        break
                    else:
                        incorrect_password = True
                        break
            if not user_found or incorrect_password:
                mb.showerror("Вход", "Неверный логин или пароль")
            return
    def validate_length(self, text):# Валидация длины вводимого текста
        if len(text) <= 10:
            return True
        else:
            return False
    def add_user(self):# Обработка события регистрации нового пользователя
        login = self.login_entry.get()
        password = self.password_entry.get()
        if not login or not password:
            mb.showwarning('Ошибка', 'Пожалуйста, заполните все поля')
            return
        else:
            if len(login) < 5 or len(password) < 7 or len(login) > 10 or len(password) > 10:
                mb.showwarning('Ошибка регистрации', 'Проверьте количество символов, возможно, оно меньше или больше допустимого.')
                return
            elif not any(char.isdigit() for char in login):
                mb.showwarning('Ошибка регистрации', 'Логин должен содержать хотя бы одну цифру.')
                return
            elif not any(char.isdigit() for char in password) or not any(char.isalpha() for char in password):
                mb.showwarning('Ошибка регистрации', 'Пароль должен содержать хотя бы одну цифру и одну букву.')
                return
        with open("DataFile.json", "r") as file:
            lines = file.readlines()
            for line in lines:
                stored_data = line.strip().split('•')
                if len(stored_data) == 2:  # Проверяем, что есть логин и пароль
                    stored_login, _ = stored_data
                    if login == stored_login:
                        mb.showwarning("Регистрация", "Пользователь с таким именем уже существует")
                        return
        with open('DataFile.json', 'a') as file:
            file.write(f'{login}•{password}\n')
            mb.showinfo('Успешная регистрация', 'Вы успешно зарегистрировались!')
            self.show_game_window()
    def show_game_window(self):# открытие окна с игрой
        self.destroy()
        second_window = GameWindow()
    def show_password(self):# Показать/скрыть пароль
        if self.password_entry.cget("show") == "*":
            self.password_entry.config(show="")
            self.toggle_password_button.config(text="Скрыть пароль")
        else:
            self.password_entry.config(show="*")
            self.toggle_password_button.config(text="Показать пароль")
class GameWindow(WindowCreate):
    def __init__(self):
        super().__init__()
        self.title("Сыграть в рендзю!")# Инициализация окна игры
        self.board_size = 15
        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        self.current_player = 1  # 1 для черного, -1 для белого
        self.first_move_completed = False
        self.is_player_turn = True
        self.player_choice = None
        self.winner = None
        self.current_player = 1
        self.create_canvas()
        self.create_mini_canvas()
        self.load_images()
        self.load_background_image()
        self.draw_board()
        self.choose_stone_color()
    def load_background_image(self):# Загрузка фона игрового поля
        self.boardIm = tk.PhotoImage(file="derevo12mini.png").subsample(1)
        self.background_image = self.canvas.create_image(456, 358, anchor=tk.CENTER, image=self.boardIm)
    def load_images(self):# Загрузка изображений для черных и белых камней
        self.black_stone_image = tk.PhotoImage(file="kamen_ne_kuzmina.png").subsample(20)
        self.white_stone_image = tk.PhotoImage(file="kamen_kuzmina.png").subsample(7)
    def create_canvas(self):# Создание игрового холста
        self.canvas = tk.Canvas(self, width=1209, height=810)
        self.canvas.place(relx=0.61, rely=0.55, anchor=tk.CENTER)
        self.canvas.bind('<Button-1>', self.click_handler)
    def create_mini_canvas(self):# Создание мини-холста с кнопками
        self.canvas_mini = tk.Canvas(self, width=225, height=350, bg='#1B493F')
        self.canvas_mini.place(relx=0.86, rely=0.48, anchor=tk.CENTER)
        self.rule_label = tk.Label(self.canvas_mini, text="Выбор цвета", font=("Helvetica", 20), bg='#1B493F', fg="white")
        self.rule_label.place(relx=0.5, rely=0.30, anchor=tk.CENTER)
        buttons = [("НАЧАТЬ ЗАНОВО", self.reset_game), ("Выйти", self.destroy)]
        for i, (text, command) in enumerate(buttons, start=1):
            button = ttk.Button(self.canvas_mini, text=text, width=25, command=command, cursor='hand2')
            button.place(relx=0.5, rely=0.65 + 0.1 * i, anchor=tk.CENTER)
    def draw_board(self):# Отрисовка игрового поля и камней
        cell_size, margin = 45, 35
        for i in range(self.board_size):
            y = margin + i * cell_size
            self.canvas.create_line(margin, y, margin + cell_size * (self.board_size - 1), y)
            for j in range(self.board_size):
                x = margin + j * cell_size
                self.canvas.create_line(x, margin, x, margin + cell_size * (self.board_size - 1))
                if self.board[i][j] != 0:
                    stone_image = self.black_stone_image if self.board[i][j] == 1 else self.white_stone_image
                    self.canvas.create_image(x, y, image=stone_image, anchor=tk.CENTER)
    def choose_stone_color(self):# Диалоговое окно для выбора цвета камней
        dop_size, c_size = 35, 45
        choice = mb.askquestion("Выбор цвета", "Вы хотите играть за черных?")
        self.current_player = 1 if choice == "yes" else -1
        self.rule_label.config(
            text='Поставьте\nпервый камень\nв центральную\n точку' if self.current_player == 1 else 'Поставьте\n белый камень')
        if self.current_player == -1:
            self.after(400, self.first_move, dop_size, c_size)
    def first_move(self, dop_size, c_size):# Ход компьютера при первом ходе, если игрок выбрал цвет белых
        self.is_player_turn = False
        if self.current_player == -1:
            self.current_bot = 1
            self.after(800, self.computer_move, dop_size, c_size)
    def click_handler(self, event):# Обработчик кликов по игровому полю
        dop_size, c_size = 35, 45
        x, y = round((event.x - dop_size) / c_size), round((event.y - dop_size) / c_size)
        if not self.is_player_turn:
            return
        if not self.first_move_completed:
            if not self.is_valid_first_move(x, y):
                return mb.showinfo("Неверный первый ход", "Первым ходом ставится чёрный камень в центр")
            self.first_move_completed = True
        elif not (0 <= x < self.board_size and 0 <= y < self.board_size and self.board[y][x] == 0):
            return mb.showinfo("Недоступный ход", "Тут уже стоит камень, выберите другое место")
        if self.current_player == -1:  # Игрок с белыми
            self.current_bot = 1
            stone_image = self.white_stone_image
            self.board[y][x] = self.current_player
            self.canvas.create_image(dop_size + x * c_size, dop_size + y * c_size, image=stone_image,
                                      anchor=tk.CENTER)
            if self.check_victory():
                self.winner = self.current_player
                self.end_game()
            else:
                self.is_player_turn = False
                self.after(800, self.computer_move, dop_size, c_size)
                self.rule_label.config(text='Ходят\n чёрные')
        else:
            self.current_bot = -1
            stone_image = self.black_stone_image
            self.board[y][x] = self.current_player
            self.canvas.create_image(dop_size + x * c_size, dop_size + y * c_size, image=stone_image,
                                      anchor=tk.CENTER)
            if self.check_victory():
                self.winner = self.current_player
                self.end_game()
            else:
                self.is_player_turn = False
                self.after(800, self.computer_move, dop_size, c_size)
                self.rule_label.config(text='Ходят\n белые')
    def is_valid_first_move(self, x, y):# Проверка, что первый ход устанавливается в центральную точку
        center = self.board_size // 2
        return x == center and y == center
    def check_victory(self):# Проверка наличия выигрышной комбинации на игровом поле
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] != 0 and self.check_direction(i, j, 1, 0, self.board[i][j]) >= 5:
                    return True  # Проверка по горизонтали
                if self.board[i][j] != 0 and self.check_direction(i, j, 0, 1, self.board[i][j]) >= 5:
                    return True  # Проверка по вертикали
                if self.board[i][j] != 0 and self.check_direction(i, j, 1, 1, self.board[i][j]) >= 5:
                    return True  # Проверка по диагонали (слева вверху вправо вниз)
                if self.board[i][j] != 0 and self.check_direction(i, j, 1, -1, self.board[i][j]) >= 5:
                    return True  # Проверка по диагонали (справа вверху влево вниз)
        return False
    def check_direction(self, row, col, delta_row, delta_col, player): # Подсчет количества одинаковых камней в направлении (delta_row, delta_col) от точки (row, col)
        count = 0
        while 0 <= row < self.board_size and 0 <= col < self.board_size and self.board[row][col] == player:
            count += 1
            row += delta_row
            col += delta_col
        return count
    def get_random_move(self):# Получение случайного хода из списка доступных ходов
        empty_cells = [(j, i) for j in range(self.board_size) for i in range(self.board_size) if self.board[i][j] == 0]
        if not empty_cells:
            return None
        random_move = random.choice(empty_cells)
        return random_move
    def computer_move(self, dop_size, c_size):# Ход компьютера
        if not self.first_move_completed and self.current_bot == 1:
            center = self.board_size // 2
            if self.board[center][center] == 0:
                self.board[center][center] = self.current_bot
                stone_image = self.black_stone_image
                self.canvas.create_image(dop_size + center * c_size, dop_size + center * c_size, image=stone_image,anchor=tk.CENTER)
                self.is_player_turn = True
                self.first_move_completed = True
            return
        best_move = self.get_random_move()
        if best_move:
            self.board[best_move[1]][best_move[0]] = self.current_bot
            stone_image = self.white_stone_image if self.current_bot == -1 else self.black_stone_image
            self.canvas.create_image(dop_size + best_move[0] * c_size, dop_size + best_move[1] * c_size, image=stone_image, anchor=tk.CENTER)
        if self.check_victory():
            self.winner = self.current_player
            self.end_game()
        else:
            self.is_player_turn = True
            self.rule_label.config(text='Ваш ход')
    def reset_game(self):# Сброс состояния игры
        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        self.canvas.delete("all")
        self.rule_label.config(text="Поставьте\nпервый камень\nв центральную\n точку")
        self.winner = None
        self.first_move_completed = False
        self.is_player_turn = True
        self.load_background_image()
        self.draw_board()
        self.current_player = 1
        self.choose_stone_color()
    def end_game(self):# Завершение игры и вывод сообщения о результате
        self.is_player_turn = True
        messages1 = {1: 'Поздравляем! Вы выиграли!', -1: 'К сожалению, вы проиграли.', 0: 'Ничья.'}
        messages2 = {-1: 'Поздравляем! Вы выиграли!', 1: 'К сожалению, вы проиграли.', 0: 'Ничья.'}
        if self.current_player == 1:
            message = messages1.get(self.winner, ' ')
        else:
            message = messages2.get(self.winner, ' ')
        if mb.askyesno('Игра окончена', f'{message} \n Сыграть ещё раз?'):
            self.reset_game()
        else:
            self.destroy()
first_window = LoginWindow() # Запуск окна входа
first_window.mainloop()
