import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from qasync import QEventLoop  # Импорт QEventLoop для интеграции asyncio с PyQt

# Асинхронные функции поиска
async def search_on_ozon():
    print("Запуск поиска на Ozon...")

    try:
        # Асинхронный запуск скрипта по указанному пути
        process = await asyncio.create_subprocess_exec(
            r"C:\Users\user\KivyFile\MarketFinds\.venv\Scripts\python.exe",
            r"C:\Users\user\PycharmProjects\OzonFind\main.py",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Ожидание завершения процесса и получение вывода
        stdout, stderr = await process.communicate()

        # Выводы процесса
        print(f"Вывод программы:\n{stdout.decode()}")
        if stderr:
            print(f"Ошибки:\n{stderr.decode()}")

    except Exception as e:
        print(f"Произошла ошибка при запуске скрипта: {e}")

    print("Поиск на Ozon завершен.")
    await asyncio.sleep(2)  # Симуляция асинхронного запроса


async def search_on_yandex():
    print("Запуск поиска на Yandex...")

    try:
        # Асинхронный запуск скрипта по указанному пути
        process = await asyncio.create_subprocess_exec(
            r"C:\Users\user\KivyFile\MarketFinds\.venv\Scripts\python.exe",
            r"C:\Users\user\PycharmProjects\YandexFind\main.py",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Ожидание завершения процесса и получение вывода
        stdout, stderr = await process.communicate()

        # Выводы процесса
        print(f"Вывод программы:\n{stdout.decode()}")
        if stderr:
            print(f"Ошибки:\n{stderr.decode()}")

    except Exception as e:
        print(f"Произошла ошибка при запуске скрипта: {e}")

    print("Поиск на Yandex завершен.")
    await asyncio.sleep(2)  # Симуляция асинхронного запроса


async def search_on_sbermegamarket():
    print("Запуск поиска на Sbermegamarket...")

    try:
        # Асинхронный запуск скрипта по указанному пути
        process = await asyncio.create_subprocess_exec(
            r"C:\Users\user\KivyFile\MarketFinds\.venv\Scripts\python.exe",
            r"C:\Users\user\PycharmProjects\SberMegaFind\main.py",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Ожидание завершения процесса и получение вывода
        stdout, stderr = await process.communicate()

        # Выводы процесса
        print(f"Вывод программы:\n{stdout.decode()}")
        if stderr:
            print(f"Ошибки:\n{stderr.decode()}")

    except Exception as e:
        print(f"Произошла ошибка при запуске скрипта: {e}")

    print("Поиск на Sbermegamarket завершен.")
    await asyncio.sleep(2)  # Симуляция асинхронного запроса


async def search_on_wildberries():
    print("Запуск поиска на Wildberries...")

    try:
        # Асинхронный запуск скрипта по указанному пути
        process = await asyncio.create_subprocess_exec(
            r"C:\Users\user\KivyFile\MarketFinds\.venv\Scripts\python.exe",
            r"C:\Users\user\PycharmProjects\WildberriesFind\main.py",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Ожидание завершения процесса и получение вывода
        stdout, stderr = await process.communicate()

        # Выводы процесса
        print(f"Вывод программы:\n{stdout.decode()}")
        if stderr:
            print(f"Ошибки:\n{stderr.decode()}")

    except Exception as e:
        print(f"Произошла ошибка при запуске скрипта: {e}")

    print("Поиск на Wildberries завершен.")
    await asyncio.sleep(2)  # Симуляция асинхронного запроса


# Основное окно приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Асинхронная форма с кнопками")
        self.setGeometry(100, 100, 300, 200)  # Устанавливаем размер окна

        layout = QVBoxLayout()  # Основной вертикальный макет

        # Создание кнопок
        self.btn_ozon = QPushButton("Запустить поиск на Ozon")
        self.btn_yandex = QPushButton("Запустить поиск на Yandex")
        self.btn_sber = QPushButton("Запустить поиск на SberMegaMarket")
        self.btn_wb = QPushButton("Запустить поиск на Wildberries")

        # Привязка кнопок к функциям
        self.btn_ozon.clicked.connect(lambda: self.run_async_task(search_on_ozon))
        self.btn_yandex.clicked.connect(lambda: self.run_async_task(search_on_yandex))
        self.btn_sber.clicked.connect(lambda: self.run_async_task(search_on_sbermegamarket))
        self.btn_wb.clicked.connect(lambda: self.run_async_task(search_on_wildberries))

        # Добавление кнопок в макет
        layout.addWidget(self.btn_ozon)
        layout.addWidget(self.btn_yandex)
        layout.addWidget(self.btn_sber)
        layout.addWidget(self.btn_wb)

        # Установка центрального виджета
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def run_async_task(self, task):
        """Запуск асинхронной задачи в основном событийном цикле."""
        asyncio.create_task(task())  # Создание и запуск задачи напрямую в событийном цикле


# Запуск приложения
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Создаем событие asyncio и интегрируем его с PyQt
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    window = MainWindow()
    window.show()

    with loop:  # Запускаем основной событийный цикл
        loop.run_forever()
