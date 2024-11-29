import json
import os
from tabulate import tabulate


class Task:
    def __init__(self, task_id, title, description, category, due_date, priority, status="Не выполнена"):
        self.id = task_id
        self.title = title
        self.description = description
        self.category = category
        self.due_date = due_date
        self.priority = priority
        self.status = status

    def mark_as_done(self):
        self.status = "Выполнена"

    def edit(self, title=None, description=None, category=None, due_date=None, priority=None):
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
            json.dump([task.to_dict() for task in self.tasks], file, ensure_ascii=False, indent=4)

    def add_task(self, title, description, category, due_date, priority):
        new_id = max((task.id for task in self.tasks), default=0) + 1
        new_task = Task(new_id, title, description, category, due_date, priority)
        self.tasks.append(new_task)
        self.save_tasks()

    def get_task_by_id(self, task_id):
        return next((task for task in self.tasks if task.id == task_id), None)

    def show_tasks(self, tasks=None):
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
    def __init__(self, manager):
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
        current_menu = "main_menu"
        while current_menu:
            current_menu = self.menus[current_menu]()

    @staticmethod
    def main_menu():
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
        print("\nДобавление задачи:")
        title = input("Название задачи: ")
        description = input("Описание задачи: ")
        category = input("Категория задачи: ")
        due_date = input("Срок выполнения (гггг-мм-дд): ")
        priority = input("Приоритет задачи (низкий, средний, высокий): ")
        self.manager.add_task(title, description, category, due_date, priority)
        print("Задача успешно добавлена!")
        return "main_menu"

    def edit_task_menu(self):
        print("\nРедактирование задачи:")
        task_id = input("Введите ID задачи для редактирования: ")
        if not task_id.isdigit():
            print("ID должен быть числом.")
            return "edit_task"
        task = self.manager.get_task_by_id(int(task_id))
        if not task:
            print("Задача с таким ID не найдена.")
            return "edit_task"

        print("\n1. Просмотреть задачу")
        print("2. Изменить задачу")
        print("3. Отметить как выполненную")
        print("4. Назад")
        choice = input("\nВыберите действие: ")

        match choice:
            case "1":
                self.manager.show_tasks([task])
                input("\nНажмите Enter для возврата в меню.")
                return "edit_task"
            case "2":
                title = input("Новое название задачи (оставьте пустым для сохранения текущего): ")
                description = input("Новое описание задачи (оставьте пустым для сохранения текущего): ")
                category = input("Новая категория задачи (оставьте пустым для сохранения текущей): ")
                due_date = input("Новый срок выполнения (оставьте пустым для сохранения текущего): ")
                priority = input("Новый приоритет задачи (оставьте пустым для сохранения текущего): ")
                task.edit(title, description, category, due_date, priority)
                self.manager.save_tasks()
                print("Задача успешно обновлена.")
                return "main_menu"
            case "3":
                task.mark_as_done()
                self.manager.save_tasks()
                print("Задача отмечена как выполненная.")
                return "main_menu"
            case "4":
                return "main_menu"
            case _:
                print("Неверный выбор. Попробуйте снова.")
                return "edit_task"

    def delete_task_menu(self):
        print("\nУдаление задач:")
        print("1. Удалить по ID")
        print("2. Удалить по категории")
        print("3. Удалить все задачи")
        print("4. Назад")
        choice = input("\nВыберите действие: ")

        match choice:
            case "1":
                task_id = input("Введите ID задачи для удаления: ")
                task = self.manager.get_task_by_id(int(task_id))
                if task:
                    self.manager.tasks.remove(task)
                    self.manager.save_tasks()
                    print("Задача удалена.")
                else:
                    print("Задача не найдена.")
                return "delete_task"
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
                    self.manager.tasks = [task for task in self.manager.tasks if task.category != selected_category]
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
        print("\nПоиск задач:")
        keyword = input("Введите ключевое слово для поиска: ")
        tasks = [task for task in self.manager.tasks if keyword.lower() in task.title.lower()]
        if tasks:
            self.manager.show_tasks(tasks)
        else:
            print("Задачи не найдены.")
        input("\nНажмите Enter для возврата в меню.")
        return "main_menu"


def main():
    task_manager = TaskManager()
    menu_handler = MenuHandler(task_manager)
    menu_handler.execute()


if __name__ == "__main__":
    main()
