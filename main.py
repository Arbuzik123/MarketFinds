import sys
import asyncio
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from qasync import QEventLoop  # Импорт QEventLoop для интеграции asyncio с PyQt
from multiprocessing import Process

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

    except Exception as e:
        print(f"Произошла ошибка при запуске скрипта: {e}")

# Функции для запуска поиска в отдельных процессах
def search_on_ozon():
    asyncio.run(run_process(r"C:\Users\user\PycharmProjects\OzonFind\main.py"))
    print("Поиск на Ozon завершен.")

def search_on_yandex():
    asyncio.run(run_process(r"C:\Users\user\PycharmProjects\YandexFind\main.py"))
    print("Поиск на Yandex завершен.")

def search_on_sbermegamarket():
    asyncio.run(run_process(r"C:\Users\user\PycharmProjects\SberMegaFind\main.py"))
    print("Поиск на Sbermegamarket завершен.")

def search_on_wildberries():
    asyncio.run(run_process(r"C:\Users\user\PycharmProjects\WildberriesFind\main.py"))
    print("Поиск на Wildberries завершен.")

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
        self.btn_ozon.clicked.connect(lambda: self.run_in_process(search_on_ozon))
        self.btn_yandex.clicked.connect(lambda: self.run_in_process(search_on_yandex))
        self.btn_sber.clicked.connect(lambda: self.run_in_process(search_on_sbermegamarket))
        self.btn_wb.clicked.connect(lambda: self.run_in_process(search_on_wildberries))

        # Добавление кнопок в макет
        layout.addWidget(self.btn_ozon)
        layout.addWidget(self.btn_yandex)
        layout.addWidget(self.btn_sber)
        layout.addWidget(self.btn_wb)

        # Установка центрального виджета
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def run_in_process(self, task):
        """Запуск задачи в отдельном процессе для изоляции."""
        process = Process(target=task)
        process.start()

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
