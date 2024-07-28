"Классы и объекты."

# Реализовать классы для взаимодействия с платформой,
# каждый из которых будет содержать методы добавления видео, авторизации и регистрации пользователя и т.д.


# Импортируем библиотеку  hashlib, которая предоставляет функции для хэширования.
# Импортируем библиотеку  time, которая предоставляет функции для работы с временем, включая задержки ( sleep).


import hashlib
import time


class User:
    def __init__(self, nickname, password, age):
        self.nickname = nickname
        self.password = hashlib.sha256(password.encode()).hexdigest() ## эта строка кода берет строку пароля, конвертирует ее в байты,
                                                                    # хэширует с использованием алгоритма SHA-256 и сохраняет полученный хэш
                                                                    #(в виде шестнадцатеричной строки) в атрибуте  self.password.

        self.age = age

    def __repr__(self):                                             #Метод  __repr__ возвращает строковое представление объекта.
        return f"User(nickname={self.nickname}, age={self.age})"


class Video:
    def __init__(self, title, duration, adult_mode=False):
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode

    def __repr__(self):
        return f"Video(title={self.title}, duration={self.duration}, adult_mode={self.adult_mode})"


class UrTube:
    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None

    def log_in(self, nickname, password):                                    #Метод  log_in выполняет вход пользователя.
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        for user in self.users:
            if user.nickname == nickname and user.password == hashed_password:
                self.current_user = user
                return
        print("Неправильный логин или пароль")

    def register(self, nickname, password, age):                            #Метод  register регистрирует нового пользователя.
        if any(user.nickname == nickname for user in self.users):
            print(f"Пользователь {nickname} уже существует")
            return
        new_user = User(nickname, password, age)
        self.users.append(new_user)
        self.current_user = new_user

    def log_out(self):                                                      #Метод  log_out выполняет выход текущего пользователя, сбрасывая.
        self.current_user = None

    def add(self, *videos):                                                 #Метод  add добавляет одно или несколько видео.
        for video in videos:
            if not any(v.title == video.title for v in self.videos):
                self.videos.append(video)

    def get_videos(self, search_word):                                      ##Метод  get_videos ищет видео по ключевому слову.
        search_word_lower = search_word.lower()
        return [video.title for video in self.videos if search_word_lower in video.title.lower()]


    def watch_video(self, title):
        if not self.current_user:
            print("Войдите в аккаунт, чтобы смотреть видео")
            return

        video = next((v for v in self.videos if v.title == title), None)

        if not video:
            print("Видео не найдено")
            return

        if video.adult_mode and self.current_user.age < 18:
            print("Вам нет 18 лет, пожалуйста покиньте страницу")
            return

        for i in range(video.time_now, video.duration):
            print(i + 1, end=' ')
            time.sleep(1)
        video.time_now = 0
        print("Конец видео")


# Код для проверки
ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')
