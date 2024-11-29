import unittest
from unittest.mock import patch
from io import StringIO
from task_manager import Task, TaskManager, MenuHandler


class TestTask(unittest.TestCase):

    def test_task_creation(self):
        """Тест на создание задачи."""
        task = Task(1, "Test Task", "Description of the task", "Category1", "2024-12-31", "Средний")

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Description of the task")
        self.assertEqual(task.category, "Category1")
        self.assertEqual(task.due_date, "2024-12-31")
        self.assertEqual(task.priority, "Средний")
        self.assertEqual(task.status, "Не выполнена")

    def test_task_edit(self):
        """Тест на редактирование задачи."""
        task = Task(1, "Test Task", "Description of the task", "Category1", "2024-12-31", "Средний")
        task.edit(title="Updated Task", description="Updated description", category="Category2", due_date="2024-11-30",
                  priority="Высокий")

        self.assertEqual(task.title, "Updated Task")
        self.assertEqual(task.description, "Updated description")
        self.assertEqual(task.category, "Category2")
        self.assertEqual(task.due_date, "2024-11-30")
        self.assertEqual(task.priority, "Высокий")

    def test_task_to_dict(self):
        """Тест на преобразование задачи в словарь."""
        task = Task(1, "Test Task", "Description", "Category1", "2024-12-31", "Средний")
        task_dict = task.to_dict()

        self.assertEqual(task_dict, {
            "id": 1,
            "title": "Test Task",
            "description": "Description",
            "category": "Category1",
            "due_date": "2024-12-31",
            "priority": "Средний",
            "status": "Не выполнена"
        })


class TestTaskManager(unittest.TestCase):

    def setUp(self):
        """Подготовка к тестам: создаем экземпляр TaskManager с временным файлом."""
        self.manager = TaskManager(file_name="test_tasks.json")
        self.manager.tasks.clear()

    def test_add_task(self):
        """Тест на добавление задачи."""
        self.manager.add_task("New Task", "Description", "Category1", "2024-12-31", "Средний")
        task = self.manager.get_task_by_id(1)

        self.assertIsNotNone(task)
        self.assertEqual(task.title, "New Task")
        self.assertEqual(task.description, "Description")
        self.assertEqual(task.category, "Category1")

    def test_get_task_by_id(self):
        """Тест на получение задачи по ID."""
        self.manager.add_task("Task 1", "Description", "Category1", "2024-12-31", "Высокий")

        task = self.manager.get_task_by_id(1)

        self.assertIsNotNone(task)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Task 1")

    def test_save_and_load_tasks(self):
        """Тест на сохранение и загрузку задач."""
        self.manager.add_task("Task 2", "Description", "Category2", "2024-12-31", "Низкий")
        self.manager.save_tasks()
        new_manager = TaskManager(file_name="test_tasks.json")

        self.assertEqual(len(new_manager.tasks), 1)
        self.assertEqual(new_manager.tasks[0].title, "Task 2")

    def test_show_tasks(self):
        """Тест на вывод задач."""
        self.manager.add_task("Task 1", "Description", "Category1", "2024-12-31", "Средний")
        self.manager.add_task("Task 2", "Description", "Category2", "2024-12-31", "Низкий")

        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            self.manager.show_tasks()
            output = mock_stdout.getvalue()

        self.assertIn("ID", output)
        self.assertIn("Task 1", output)
        self.assertIn("Task 2", output)


class TestMenuHandler(unittest.TestCase):

    @patch("builtins.input", side_effect=["1"])
    def test_main_menu(self, mock_input):
        """Тест на выбор пунктов в главном меню."""
        task_manager = TaskManager(file_name="test_tasks.json")
        menu_handler = MenuHandler(task_manager)

        # Вызов метода main_menu
        menu_handler.main_menu()

        # Проверка, что метод выбора пункта меню был вызван
        mock_input.assert_called_once_with('\nВыберите действие: ')


if __name__ == "__main__":
    unittest.main()
