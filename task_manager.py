import json
import os
from tabulate import tabulate


class Task:
    """
    Класс для представления задачи.

    Атрибуты:
        id (int): Уникальный идентификатор задачи.
        Title (str): Название задачи.
        Description (str): Описание задачи.
        Category (str): Категория задачи.
        Due_date (str): Срок выполнения задачи (в формате гггг-мм-дд).
        Priority (str): Приоритет задачи (низкий, средний, высокий).
        Status (str): Статус задачи (по умолчанию "Не выполнена").
    """

    def __init__(self, task_id, title, description, category, due_date, priority, status="Не выполнена"):
        """
        Инициализация задачи.

        :param task_id: Уникальный идентификатор задачи.
        :param title: Название задачи.
        :param description: Описание задачи.
        :param category: Категория задачи.
        :param due_date: Срок выполнения задачи.
        :param priority: Приоритет задачи.
        :param status: Статус задачи.
        """
        self.id = task_id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def mark_as_done(self):
        """
        Отметить задачу как выполненную.
        """
        self.status = "Выполнена"

    def edit(self, title=None, description=None, category=None, due_date=None, priority=None):
        """
        Редактировать задачу.

        :param title: Новое название задачи.
        :param description: Новое описание задачи.
        :param category: Новая категория задачи.
        :param due_date: Новый срок выполнения задачи.
        :param priority: Новый приоритет задачи.
        """
        if title:
            self.title = title
        if description:
            self.description = description
        if category:
            self.category = category
        if due_date:
            self.due_date = due_date
        if priority:
            self.priority = priority

    def to_dict(self):
        """
        Преобразовать задачу в словарь.

        :return: Словарь с данными задачи.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
        }

    @staticmethod
    def from_dict(data):
        """
        Создать задачу из словаря.

        :param data: Словарь с данными задачи.
        :return: Экземпляр задачи.
        """
        return Task(
            task_id=data["id"],
            title=data["title"],
            description=data["description"],
            category=data["category"],
            due_date=data["due_date"],
            priority=data["priority"],
            status=data["status"],
        )


class TaskManager:
    """
    Класс для управления задачами.

    Атрибуты:
        File_name (str): Имя файла для хранения задач.
        Tasks (list): Список задач.
    """

    def __init__(self, file_name="tasks.json"):
        """
        Инициализация менеджера задач.

        :param file_name: Имя файла для хранения задач.
        """
        self.file_name = file_name
        self.tasks = self.load_tasks()

    def load_tasks(self):
        """
        Загрузить задачи из файла.

        :return: Список задач.
        """
        if os.path.exists(self.file_name):
            with open(self.file_name, "r", encoding="utf-8") as file:
                return [Task.from_dict(task) for task in json.load(file)]
        return []

    def save_tasks(self):
        """
        Сохранить задачи в файл.
        """
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False, indent=4)

    def add_task(self, title, description, category, due_date, priority):
        """
        Добавить новую задачу.

        :param title: Название задачи.
        :param description: Описание задачи.
        :param category: Категория задачи.
        :param due_date: Срок выполнения задачи.
        :param priority: Приоритет задачи.
        """
        new_id = max((task.id for task in self.tasks), default=0) + 1
        new_task = Task(new_id, title, description, category, due_date, priority)
        self.tasks.append(new_task)
        self.save_tasks()

    def get_task_by_id(self, task_id):
        """
        Получить задачу по ID.

        :param task_id: Идентификатор задачи.
        :return: Задача с данным ID или None, если не найдена.
        """
        return next((task for task in self.tasks if task.id == task_id), None)

    def show_tasks(self, tasks=None):
        """
        Показать список задач.

        :param tasks: Список задач для отображения. Если None, показываются все задачи.
        """
        if not tasks:
            tasks = self.tasks
        if not tasks:
            print("Список задач пуст.")
            return
        table = [
            [task.id, task.title, task.category, task.due_date, task.priority, task.status]
            for task in tasks
        ]
        headers = ["ID", "Название", "Категория", "Срок", "Приоритет", "Статус"]
        print(tabulate(table, headers=headers, tablefmt="grid"))


class MenuHandler:
    """
    Класс для управления меню приложения.

    Атрибуты:
        Manager (TaskManager): Менеджер задач.
        Menus (dict): Словарь с пунктами меню и их обработчиками.
    """

    def __init__(self, manager):
        """
        Инициализация MenuHandler.

        :param manager: Менеджер задач.
        """
        self.manager = manager
        self.menus = {
            "main_menu": self.main_menu,
            "view_tasks": self.view_tasks_menu,
            "add_task": self.add_task_menu,
            "edit_task": self.edit_task_menu,
            "delete_task": self.delete_task_menu,
            "search_task": self.search_task_menu,
        }

    def execute(self):
        """
        Запуск меню.

        Отображает меню и вызывает соответствующие методы на основе выбора пользователя.
        """
        current_menu = "main_menu"
        while current_menu:
            current_menu = self.menus[current_menu]()

    @staticmethod
    def main_menu():
        """
        Главное меню приложения.

        :return: Следующее меню, в зависимости от выбора пользователя.
        """
        print("\nГлавное меню:")
        print("1. Просмотр задач")
        print("2. Добавить задачу")
        print("3. Изменить задачу")
        print("4. Удалить задачу")
        print("5. Поиск задач")
        print("6. Выход")
        choice = input("\nВыберите действие: ")

        match choice:
            case "1":
                return "view_tasks"
            case "2":
                return "add_task"
            case "3":
                return "edit_task"
            case "4":
                return "delete_task"
            case "5":
                return "search_task"
            case "6":
                print("Выход из программы.")
                return None
            case _:
                print("Неверный выбор. Попробуйте снова.")
                return "main_menu"

    def view_tasks_menu(self):
        """
        Меню просмотра задач.

        :return: Следующее меню, в зависимости от выбора пользователя.
        """
        print("\nПросмотр задач:")
        print("1. Все задачи")
        print("2. По категории")
        print("3. Назад")
        choice = input("\nВыберите действие: ")

        match choice:
            case "1":
                self.manager.show_tasks()
                input("\nНажмите Enter для возврата в меню.")
                return "view_tasks"
            case "2":
                categories = {task.category for task in self.manager.tasks}
                if not categories:
                    print("Категории отсутствуют.")
                else:
                    print("\nКатегории:")
                    for idx, category in enumerate(categories, start=1):
                        print(f"{idx}. {category}")
                    category = input("\nВведите категорию или номер: ")
                    selected_category = (
                        list(categories)[int(category) - 1]
                        if category.isdigit() and 0 < int(category) <= len(categories)
                        else category
                    )
                    tasks = [task for task in self.manager.tasks if task.category == selected_category]
                    self.manager.show_tasks(tasks)
                input("\nНажмите Enter для возврата в меню.")
                return "view_tasks"
            case "3":
                return "main_menu"
            case _:
                print("Неверный выбор. Попробуйте снова.")
                return "view_tasks"

    def add_task_menu(self):
        """
        Меню добавления задачи.

        :return: Главное меню после добавления задачи.
        """
        print("\nДобавление задачи:")
        title = input("Название задачи: ")
        description = input("Описание задачи: ")
        category = input("Категория задачи: ")
        due_date = input("Срок выполнения (гггг-мм-дд): ")
        priority = input("Приоритет задачи (низкий, средний, высокий): ")

        self.manager.add_task(title, description, category, due_date, priority)
        print("Задача добавлена.")
        input("\nНажмите Enter для возврата в меню.")
        return "main_menu"

    def edit_task_menu(self):
        """
        Меню редактирования задачи.

        :return: Главное меню после редактирования задачи.
        """
        print("\nРедактирование задачи:")
        task_id = int(input("Введите ID задачи для редактирования: "))
        task = self.manager.get_task_by_id(task_id)
        if task:
            title = input(f"Новое название ({task.title}): ")
            description = input(f"Новое описание ({task.description}): ")
            category = input(f"Новая категория ({task.category}): ")
            due_date = input(f"Новый срок выполнения ({task.due_date}): ")
            priority = input(f"Новый приоритет ({task.priority}): ")
            task.edit(title, description, category, due_date, priority)
            self.manager.save_tasks()
            print("Задача обновлена.")
        else:
            print("Задача не найдена.")
        input("\nНажмите Enter для возврата в меню.")
        return "main_menu"

    def delete_task_menu(self):
        """
        Меню удаления задач.

        :return: Главное меню после удаления задачи.
        """
        print("\nУдаление задачи:")
        print("1. Удалить задачу по ID")
        print("2. Удалить задачи по категории")
        print("3. Удалить все задачи")
        print("4. Назад")
        choice = input("\nВыберите действие: ")

        match choice:
            case "1":
                task_id = int(input("Введите ID задачи для удаления: "))
                task = self.manager.get_task_by_id(task_id)
                if task:
                    self.manager.tasks.remove(task)
                    self.manager.save_tasks()
                    print("Задача удалена.")
                else:
                    print("Задача не найдена.")
                return "delete_task"
            case "2":
                category = input("Введите категорию для удаления: ")
                tasks_to_delete = [task for task in self.manager.tasks if task.category == category]
                for task in tasks_to_delete:
                    self.manager.tasks.remove(task)
                self.manager.save_tasks()
                print("Задачи из категории удалены.")
                return "delete_task"
            case "3":
                self.manager.tasks.clear()
                self.manager.save_tasks()
                print("Все задачи удалены.")
                return "delete_task"
            case "4":
                return "main_menu"
            case _:
                print("Неверный выбор. Попробуйте снова.")
                return "delete_task"

    def search_task_menu(self):
        """
        Меню поиска задач по ключевому слову, категории или статусу.

        :return: Главное меню после поиска.
        """
        while True:
            print("\nПоиск задач:")
            print("1. Поиск по ключевому слову в названии задачи")
            print("2. Поиск по категории")
            print("3. Поиск по статусу выполнения")
            print("4. Назад")
            choice = input("\nВыберите действие: ")

            if choice == "1":
                keyword = input("Введите ключевое слово для поиска: ")
                tasks = [task for task in self.manager.tasks if keyword.lower() in task.title.lower()]
                if tasks:
                    self.manager.show_tasks(tasks)
                else:
                    print("Задачи не найдены по ключевому слову.")
                input("\nНажмите Enter для возврата в меню поиска.")

            elif choice == "2":
                categories = {task.category for task in self.manager.tasks}
                if not categories:
                    print("Категории отсутствуют.")
                else:
                    print("\nКатегории:")
                    # Выводим категории с номерами
                    category_list = list(categories)
                    for idx, category in enumerate(category_list, start=1):
                        print(f"{idx}. {category}")

                    # Получаем ввод пользователя
                    category_input = input("\nВведите категорию для поиска или номер категории: ")

                    # Проверка, если введен номер категории
                    if category_input.isdigit() and 0 < int(category_input) <= len(category_list):
                        selected_category = category_list[int(category_input) - 1]
                    else:
                        selected_category = category_input.strip()

                    # Фильтрация задач по выбранной категории
                    tasks = [task for task in self.manager.tasks if task.category.lower() == selected_category.lower()]
                    if tasks:
                        self.manager.show_tasks(tasks)  # Выводим задачи по выбранной категории
                    else:
                        print("Задачи не найдены по выбранной категории.")
                input("\nНажмите Enter для возврата в меню поиска.")

            elif choice == "3":
                # Предоставим пользователю выбор статуса
                print("\nСтатусы задач:")
                print("1. Не выполнена")
                print("2. Выполнена")
                status_choice = input("Выберите статус для поиска (1 или 2): ")

                if status_choice == "1":
                    status = "Не выполнена"
                elif status_choice == "2":
                    status = "Выполнена"
                else:
                    print("Неверный выбор. Попробуйте снова.")
                    continue

                tasks = [task for task in self.manager.tasks if task.status.lower() == status.lower()]
                if tasks:
                    self.manager.show_tasks(tasks)  # Выводим задачи с выбранным статусом
                else:
                    print(f"Задачи со статусом '{status}' не найдены.")
                input("\nНажмите Enter для возврата в меню поиска.")

            elif choice == "4":
                return "main_menu"

            else:
                print("Неверный выбор. Попробуйте снова.")


def main():
    """
    Главная функция для запуска приложения.

    Создает экземпляры менеджера задач и обработчика меню, затем запускает меню.
    """
    task_manager = TaskManager()
    menu_handler = MenuHandler(task_manager)
    menu_handler.execute()


if __name__ == "__main__":
    main()
