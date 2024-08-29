import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from qasync import QEventLoop
from multiprocessing import Process
import time

# Функция для запуска внешнего скрипта
async def run_process(script_path):
    """Асинхронный запуск внешнего скрипта и вывод его результатов в реальном времени."""
    try:
        process = await asyncio.create_subprocess_exec(
            r"C:\Users\user\KivyFile\MarketFinds\.venv\Scripts\python.exe",
            script_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        # Асинхронное чтение и вывод stdout и stderr в реальном времени
        while True:
            stdout_line = await process.stdout.readline()
            stderr_line = await process.stderr.readline()

            if not stdout_line and not stderr_line:
                break

            if stdout_line:
                print(stdout_line.decode().strip())

            if stderr_line:
                print(stderr_line.decode().strip())

        await process.wait()  # Ожидание завершения процесса

    except asyncio.CancelledError:
        print("Асинхронная задача была отменена.")
    except Exception as e:
        print(f"Произошла ошибка при запуске скрипта: {e}")


# Функции для запуска поиска в отдельных процессах с задержкой
def search_on_ozon():
    asyncio.run(run_process(r"C:\Users\user\PycharmProjects\OzonFind\main.py"))
    print("Поиск на Ozon завершен.")


def search_on_yandex():
    asyncio.run(run_process(r"C:\Users\user\PycharmProjects\YandexFind\main.py"))
    print("Поиск на Yandex завершен.")


def search_on_sbermegamarket():
    asyncio.run(run_process(r"C:\Users\user\PycharmProjects\SberMegaFind\main.py"))
    print("Поиск на SberMegaMarket завершен.")


def search_on_wildberries():
    asyncio.run(run_process(r"C:\Users\user\PycharmProjects\WildberriesFind\main.py"))
    print("Поиск на Wildberries завершен.")


# Функция, вызываемая после завершения всех процессов
def all_processes_done():
    print("Все поисковые процессы завершены.")


# Основное окно приложения
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Асинхронная форма с кнопками")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        # Создание кнопок
        self.btn_ozon = QPushButton("Запустить поиск на Ozon")
        self.btn_yandex = QPushButton("Запустить поиск на Yandex")
        self.btn_sber = QPushButton("Запустить поиск на SberMegaMarket")
        self.btn_wb = QPushButton("Запустить поиск на Wildberries")
        self.btn_run_all = QPushButton("Запустить все поиски")

        # Привязка кнопок к функциям
        self.btn_ozon.clicked.connect(lambda: self.run_in_process(search_on_ozon))
        self.btn_yandex.clicked.connect(lambda: self.run_in_process(search_on_yandex))
        self.btn_sber.clicked.connect(lambda: self.run_in_process(search_on_sbermegamarket))
        self.btn_wb.clicked.connect(lambda: self.run_in_process(search_on_wildberries))
        self.btn_run_all.clicked.connect(self.run_all_searches)

        # Добавление кнопок в макет
        layout.addWidget(self.btn_ozon)
        layout.addWidget(self.btn_yandex)
        layout.addWidget(self.btn_sber)
        layout.addWidget(self.btn_wb)
        layout.addWidget(self.btn_run_all)

        # Установка центрального виджета
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Менеджер для отслеживания процессов
        self.processes = []

    def run_in_process(self, task):
        """Запуск задачи в отдельном процессе для изоляции."""
        process = Process(target=task)
        self.processes.append(process)
        process.start()

    def run_all_searches(self):
        """Запуск всех поисков с задержкой для предотвращения конфликтов."""
        tasks = [search_on_ozon, search_on_yandex, search_on_sbermegamarket, search_on_wildberries]

        # Запускаем все процессы с задержкой в 1 секунду
        for task in tasks:
            self.run_in_process(task)
            time.sleep(1)  # Задержка перед запуском следующего процесса

        # Ждем завершения всех процессов и вызываем функцию завершения
        self.check_processes_completion()

    def check_processes_completion(self):
        """Проверка завершения всех процессов."""
        for process in self.processes:
            process.join()  # Ждем завершения каждого процесса

        # Вызываем функцию завершения
        all_processes_done()


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
