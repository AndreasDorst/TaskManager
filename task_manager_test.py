import os
import unittest
from unittest.mock import patch
from task_manager import Task, TaskManager, ViewTasks


class TestTaskManager(unittest.TestCase):
    def setUp(self):
        """Инициализация для тестов"""
        self.manager = TaskManager(file_name="test_tasks.json")
        self.test_task_data = {
            "task_id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "category": "Work",
            "due_date": "2024-12-01",
            "priority": "High",
            "status": "Не выполнена",
        }

    def test_create_task(self):
        """Тестирование создания задачи"""
        task = Task(
            task_id=self.test_task_data["task_id"],
            title=self.test_task_data["title"],
            description=self.test_task_data["description"],
            category=self.test_task_data["category"],
            due_date=self.test_task_data["due_date"],
            priority=self.test_task_data["priority"],
            status=self.test_task_data["status"],
        )

        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.category, "Work")
        self.assertEqual(task.due_date, "2024-12-01")
        self.assertEqual(task.priority, "High")
        self.assertEqual(task.status, "Не выполнена")

    def test_task_to_dict(self):
        """Тестирование метода to_dict()"""
        task = Task(**self.test_task_data)
        task_dict = task.to_dict()
        self.assertEqual(task_dict["id"], 1)
        self.assertEqual(task_dict["title"], "Test Task")
        self.assertEqual(task_dict["description"], "Test Description")
        self.assertEqual(task_dict["category"], "Work")
        self.assertEqual(task_dict["due_date"], "2024-12-01")
        self.assertEqual(task_dict["priority"], "High")
        self.assertEqual(task_dict["status"], "Не выполнена")

    def test_task_from_dict(self):
        """Тестирование метода from_dict()"""
        task_dict = self.test_task_data
        task = Task.from_dict(task_dict)
        self.assertEqual(task.id, 1)
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.description, "Test Description")
        self.assertEqual(task.category, "Work")
        self.assertEqual(task.due_date, "2024-12-01")
        self.assertEqual(task.priority, "High")
        self.assertEqual(task.status, "Не выполнена")

    def test_mark_task_as_done(self):
        """Тестирование метода mark_as_done()"""
        task = Task(**self.test_task_data)
        task.mark_as_done()
        self.assertEqual(task.status, "Выполнена")

    def test_add_task(self):
        """Тестирование добавления задачи в TaskManager"""
        task_data = self.test_task_data
        task = Task(**task_data)
        self.manager.tasks.append(task)
        self.manager.save_tasks()

        loaded_task = self.manager.get_task_by_id(1)
        self.assertIsNotNone(loaded_task)
        self.assertEqual(loaded_task.id, 1)
        self.assertEqual(loaded_task.title, "Test Task")

    def test_get_task_by_id(self):
        """Тестирование получения задачи по ID"""
        task_data = self.test_task_data
        task = Task(**task_data)
        self.manager.tasks.append(task)
        self.manager.save_tasks()

        loaded_task = self.manager.get_task_by_id(1)
        self.assertEqual(loaded_task.id, 1)
        self.assertEqual(loaded_task.title, "Test Task")

    def test_load_tasks(self):
        """Тестирование загрузки задач из файла"""
        task_data = self.test_task_data
        task = Task(**task_data)
        self.manager.tasks.append(task)
        self.manager.save_tasks()

        manager2 = TaskManager(file_name="test_tasks.json")
        self.assertEqual(len(manager2.tasks), 1)
        self.assertEqual(manager2.tasks[0].id, 1)

    @patch("builtins.input", return_value="1")
    def test_view_task_menu(self, ):
        """Тестирование вызова меню отображения задач"""
        with patch("builtins.print") as mock_print:
            view_tasks = ViewTasks(self.manager)
            view_tasks.execute()
            mock_print.assert_called_with("1. Просмотр всех задач")

    def tearDown(self):
        """Удаление временных файлов после тестов"""
        if os.path.exists("test_tasks.json"):
            os.remove("test_tasks.json")


if __name__ == "__main__":
    unittest.main()
