import json
import os
from tabulate import tabulate


class Task:
    def __init__(
        self,
        task_id,
        title,
        description,
        category,
        due_date,
        priority,
        status="Не выполнена",
    ):
        self.id = task_id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def mark_as_done(self):
        self.status = "Выполнена"

    def edit(
        self, title=None, description=None, category=None, due_date=None, priority=None
    ):
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

    def mark_as_done(self):
        self.status = "Выполнена"

    def to_dict(self):
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
    def __init__(self, file_name="tasks.json"):
        self.file_name = file_name
        self.tasks = self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, "r", encoding="utf-8") as file:
                return [Task.from_dict(task) for task in json.load(file)]
        return []

    def save_tasks(self):
        with open(self.file_name, "w", encoding="utf-8") as file:
            json.dump(
                [task.to_dict() for task in self.tasks],
                file,
                ensure_ascii=False,
                indent=4,
            )

    def get_task_by_id(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def show_tasks(self, tasks=None):
        """Вывод всех задач или переданных задач в виде таблицы."""
        if not tasks:
            tasks = self.tasks

        task = tasks[0]
        table = [
            [
                task.id,
                task.title,
                task.category,
                task.due_date,
                task.priority,
                task.status,
            ]
            for task in tasks
        ]
        headers = ["ID", "Название", "Категория", "Срок", "Приоритет", "Статус"]

        print(tabulate(table, headers=headers, tablefmt="grid"))


class ViewTasks:
    def __init__(self, manager):
        self.manager = manager

    def execute(self):
        while True:  # Цикл для повторного отображения меню
            print("\n1. Просмотр всех задач")
            print("2. Просмотр задач по категориям")
            print("3. Выход в главное меню\n")
            choice = input("Выберите опцию: ")

            match choice:
                case "1":
                    self.manager.show_tasks()  # Показать все задачи
                    input("\nНажмите Enter для возврата в подменю...")
                case "2":
                    self.view_tasks_by_category()  # Показать задачи по категории
                    input("\nНажмите Enter для возврата в подменю...")
                case "3":
                    print("Выход в главное меню...")
                    return  # Возврат в главное меню
                case _:
                    print("Неверный выбор! Попробуйте снова.")

    def view_tasks_by_category(self):
        categories = {task.category for task in self.manager.tasks}
        if categories:
            # Нумерация категорий
            print("\nДоступные категории:\n")
            for idx, category in enumerate(categories, start=1):
                print(f"{idx}. {category}")
            category_choice = input(
                "\nВведите категорию или номер (или Enter для отмены): "
            )
            if category_choice:
                # Проверка выбора по номеру или строке
                category = (
                    list(categories)[int(category_choice) - 1]
                    if category_choice.isdigit()
                    and 0 < int(category_choice) <= len(categories)
                    else category_choice
                )
                tasks_in_category = [
                    task
                    for task in self.manager.tasks
                    if task.category.lower() == category.lower()
                ]
                if tasks_in_category:
                    self.manager.show_tasks(
                        tasks_in_category
                    )  # Показать задачи по категории
                else:
                    print("Задачи не найдены в выбранной категории.")
            else:
                print("Отмена просмотра.")
        else:
            print("Нет доступных категорий.")


class AddTask:
    def __init__(self, manager):
        self.manager = manager

    def execute(self):
        title = input("\nНазвание задачи: ")
        description = input("Описание задачи: ")
        category = input("Категория: ")
        due_date = input("Срок выполнения (гггг-мм-дд): ")
        priority = input("Приоритет (низкий, средний, высокий): ")

        # Добавляем задачу через менеджер
        self.manager.add_task(title, description, category, due_date, priority)
        print("Задача добавлена!")


class EditTask:
    def __init__(self, manager):
        self.manager = manager

    def execute(self):
        # Ввод ID задачи для редактирования
        while True:
            task_id_input = input("\nID задачи для редактирования: ")

            # Валидация: проверяем, является ли введённое значение числом
            if not task_id_input.isdigit():
                print("Ошибка: ID должен быть числом.")
                continue  # Запрашиваем ID снова, если введено не число

            task_id = int(task_id_input)

            # Проверяем, существует ли задача с таким ID
            task = self.manager.get_task_by_id(task_id)
            if not task:
                print(f"Задача с ID {task_id} не найдена.")
                continue  # Запрашиваем ID снова, если задача не найдена

            break  # Выход из цикла, если ID валидный и задача найдена

        # Подменю для изменения задачи
        while True:
            print("\n1. Просмотр текущих данных задачи")
            print("2. Отметить задачу как выполненную")
            print("3. Изменить задачу")
            print("4. Назад\n")
            choice = input("Выберите действие: ")

            match choice:
                case "1":
                    # Вывод текущих данных задачи в виде таблицы
                    print("Текущие данные задачи:")
                    self.manager.show_tasks([task])
                case "2":
                    # Отметить задачу как выполненную
                    task.mark_as_done()
                    self.manager.save_tasks()
                    print("Задача отмечена как выполненная!")
                case "3":
                    # Редактирование задачи
                    title = input(
                        "Новое название (оставьте пустым для без изменений): "
                    )
                    description = input(
                        "Новое описание (оставьте пустым для без изменений): "
                    )
                    category = input(
                        "Новая категория (оставьте пустым для без изменений): "
                    )
                    due_date = input(
                        "Новый срок выполнения (оставьте пустым для без изменений): "
                    )
                    priority = input(
                        "Новый приоритет (оставьте пустым для без изменений): "
                    )

                    # Редактируем задачу, если введены новые данные
                    task.edit(title, description, category, due_date, priority)

                    # Сохраняем изменения
                    self.manager.save_tasks()
                    print("Задача обновлена!")
                case "4":
                    # Выход из подменю
                    print("Возвращаемся в главное меню...")
                    return  # Выход в главное меню
                case _:
                    print(
                        "Неверный выбор! Пожалуйста, выберите один из предложенных вариантов."
                    )


class MarkTaskDone:
    def __init__(self, manager):
        self.manager = manager

    def execute(self):
        task_id_input = input("ID задачи для отметки как выполненной: ")

        # Валидация: проверяем, является ли введённое значение числом
        if not task_id_input.isdigit():
            print("Ошибка: ID должен быть числом.")
            return

        task_id = int(task_id_input)

        # Проверяем, существует ли задача с таким ID
        task = self.manager.get_task_by_id(task_id)
        if not task:
            print(f"Задача с ID {task_id} не найдена.")
            return

        # Отмечаем задачу как выполненную
        task.mark_as_done()

        # Сохраняем изменения
        self.manager.save_tasks()
        print("Задача отмечена как выполненная!")


class DeleteTask:
    def __init__(self, manager):
        self.manager = manager

    def execute(self):
        while (
            True
        ):  # Повторяем меню удаления до тех пор, пока не выберется правильное действие
            print("\n1. Удаление задачи по ID")
            print("2. Удаление задач по категории")
            print("3. Удаление всех задач")
            print("4. Отмена (вернуться в главное меню)\n")
            choice = input("Выберите опцию: ")

            match choice:
                case "1":
                    task_id = input(
                        "Введите ID задачи для удаления (или Enter для отмены): "
                    )
                    if task_id:
                        task = self.manager.get_task_by_id(int(task_id))
                        if task:
                            confirmation = input(
                                f"Вы уверены, что хотите удалить задачу с ID {task_id}? (да/нет): "
                            )
                            if confirmation.lower() == "да":
                                self.manager.tasks.remove(task)
                                self.manager.save_tasks()
                                print("Задача удалена!")
                            else:
                                print("Удаление отменено.")
                        else:
                            print("Задача не найдена.")
                    else:
                        print("Отмена удаления.")
                case "2":
                    categories = {task.category for task in self.manager.tasks}
                    if categories:
                        # Нумерация категорий
                        print("\nДоступные категории для удаления:\n")
                        for idx, category in enumerate(categories, start=1):
                            print(f"{idx}. {category}")
                        category_choice = input(
                            "\nВведите категорию или номер (или Enter для отмены): "
                        )
                        if category_choice:
                            # Проверка выбора по номеру или строке
                            category = (
                                list(categories)[int(category_choice) - 1]
                                if category_choice.isdigit()
                                and 0 < int(category_choice) <= len(categories)
                                else category_choice
                            )
                            tasks_in_category = [
                                task
                                for task in self.manager.tasks
                                if task.category.lower() == category.lower()
                            ]
                            if tasks_in_category:
                                confirmation = input(
                                    f"Вы уверены, что хотите удалить все задачи в категории '{category}'? (да/нет): "
                                )
                                if confirmation.lower() == "да":
                                    for task in tasks_in_category:
                                        self.manager.tasks.remove(task)
                                    self.manager.save_tasks()
                                    print(f"Задачи в категории '{category}' удалены!")
                                else:
                                    print("Удаление отменено.")
                            else:
                                print("Задачи не найдены.")
                        else:
                            print("Отмена удаления.")
                    else:
                        print("Нет доступных категорий.")
                case "3":
                    confirmation = input(
                        "Вы уверены, что хотите удалить все задачи? (да/нет): "
                    )
                    if confirmation.lower() == "да":
                        self.manager.tasks.clear()
                        self.manager.save_tasks()
                        print("Все задачи удалены!")
                    else:
                        print("Удаление отменено.")
                case "4":
                    print("Возвращаемся в меню удаления задач...")
                    return  # Возвращение в меню удаления

                case _:
                    print("Неверный выбор! Попробуйте снова.")

        # Плавный возврат в меню, последовательно
        return "main_menu"  # Вернем к главному меню


class SearchTask:
    def __init__(self, manager):
        self.manager = manager

    def search_tasks(self, keyword=None, category=None, status=None):
        """Поиск задач по ключевому слову, категории или статусу."""
        result = self.manager.tasks

        if keyword:
            # Поиск по полному совпадению ключевого слова в title или description
            result = [
                task
                for task in result
                if keyword.lower() == task.title.lower()
                or keyword.lower() == task.description.lower()
            ]

        if category:
            result = [
                task for task in result if category.lower() == task.category.lower()
            ]

        if status:
            result = [task for task in result if status.lower() == task.status.lower()]

        return result

    def execute(self):
        while True:  # Цикл, чтобы снова возвращаться в подменю поиска
            print("\n1. Поиск по ключевому слову")
            print("2. Поиск по категории")
            print("3. Поиск по статусу")
            print("4. Вернуться в главное меню")
            choice = input("\nВыберите опцию: ")

            match choice:
                case "1":
                    keyword = input("Введите ключевое слово: ")
                    result = self.search_tasks(keyword=keyword)
                    if result:
                        self.manager.show_tasks(result)
                    else:
                        print("Поиск не дал результатов.")
                case "2":
                    categories = {task.category for task in self.manager.tasks}
                    if not categories:
                        print("Нет доступных категорий!")
                    else:
                        print("Доступные категории:")
                        for idx, category in enumerate(categories, start=1):
                            print(f"{idx}. {category}")
                        category_choice = input(
                            "Введите название категории или номер: "
                        )
                        category = (
                            list(categories)[int(category_choice) - 1]
                            if category_choice.isdigit()
                            and 0 < int(category_choice) <= len(categories)
                            else category_choice
                        )
                        result = self.search_tasks(category=category)
                        if result:
                            self.manager.show_tasks(result)
                        else:
                            print("Поиск не дал результатов.")
                case "3":
                    print("1. Выполнена")
                    print("2. Не выполнена")
                    status_choice = input("Выберите статус для поиска: ")

                    status = None
                    match status_choice:
                        case "1":
                            status = "Выполнена"
                        case "2":
                            status = "Не выполнена"
                        case _:
                            print("Неверный выбор!")
                            continue  # Продолжаем цикл, чтобы снова предложить правильный выбор

                    result = self.search_tasks(status=status)
                    if result:
                        self.manager.show_tasks(result)
                    else:
                        print("Поиск не дал результатов.")
                case "4":
                    print("Возвращаемся в главное меню...")
                    break  # Выход из подменю и возврат в главное меню
                case _:
                    print("Неверный выбор!")

            input("Нажмите Enter для возврата в подменю поиска...")  # Возврат в подменю


def main():
    manager = TaskManager()
    program_name = r"""
    ▀█▀ ▄▀█ █▀ █▄▀   █▀▄▀█ ▄▀█ █▄░█ ▄▀█ █▀▀ █▀▀ █▀█
    ░█░ █▀█ ▄█ █░█   █░▀░█ █▀█ █░▀█ █▀█ █▄█ ██▄ █▀▄
    """

    actions = {
        "1": ViewTasks(manager),
        "2": AddTask(manager),
        "3": EditTask(manager),
        "4": DeleteTask(manager),
        "5": SearchTask(manager),
    }

    while True:
        print(program_name)
        print("1. Просмотр задач")
        print("2. Добавить задачу")
        print("3. Изменить задачу")
        print("4. Удалить задачу")
        print("5. Поиск задач")
        print("6. Выход\n")

        choice = input("Выберите действие: ")

        if choice == "6":
            print("Выход из программы...")
            break

        action = actions.get(choice)
        if action:
            action.execute()
        else:
            print(
                "Неверный выбор. Пожалуйста, выберите один из предложенных вариантов."
            )


if __name__ == "__main__":
    main()
