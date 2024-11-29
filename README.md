# Приложение "Менеджер задач"

Это простое консольное приложение, написанное на Python, которое позволяет управлять задачами с возможностью добавления,
редактирования, удаления и поиска задач. Задачи сохраняются в файл JSON.

## Возможности

- **Просмотр задач**: Отображение всех задач или фильтрация по категории.
- **Добавление задач**: Создание новых задач с указанием названия, описания, категории, срока выполнения и приоритета.
- **Редактирование задач**: Изменение данных существующих задач.
- **Удаление задач**: Удаление задач по ID, категории или удаление всех задач.
- **Поиск задач**: Поиск задач по ключевому слову в названии.
- **Система приоритетов**: Назначение приоритета задачам (низкий, средний, высокий).
- **Отслеживание статуса**: Отметить задачи как выполненные.

## Требования

- Python 3.x
- Библиотека `tabulate` (используется для отображения списка задач в табличном формате)

Для установки зависимостей выполните команду:

```bash
pip install tabulate
```

## Установка и настройка проекта

1. Склонируйте репозиторий с помощью Git:

   ```bash
   git clone https://github.com/AndreasDorst/TaskManager.git
   ```

2. Перейдите в директорию проекта:

   ```bash
   cd task-manager
   ```

3. Установите необходимые зависимости:

   Для этого создайте и активируйте виртуальное окружение:

    - Для Windows:
      ```bash
      python -m venv venv
      venv\Scriptsctivate
      ```

    - Для macOS/Linux:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```

4. Установите зависимости из `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```

   ```bash
   pip install tabulate
   ```

5. Запустите приложение:

   ```bash
   python task_manager.py
   ```

## Структура файлов

- `task_manager.py`: Основной файл с кодом, содержащий классы `Task`, `TaskManager` и `MenuHandler`.
- `tasks.json`: JSON файл для хранения всех задач. (Этот файл будет автоматически создан после добавления задач.)
- `example.json`: Содержит пример данных.

## Как использовать

1. Запустите приложение, выполнив следующую команду:

   ```bash
   python task_manager.py
   ```

2. Приложение отобразит **Основное меню** с несколькими опциями:
    - Просмотр задач
    - Добавить задачу
    - Изменить задачу
    - Удалить задачу
    - Поиск задачи
    - Выход

3. Вы можете взаимодействовать с приложением, выбирая соответствующие опции и следуя подсказкам для управления задачами.

### Пример структуры задачи:

Каждая задача имеет следующие атрибуты:

- **ID**: Уникальный идентификатор задачи.
- **Название**: Название задачи.
- **Описание**: Краткое описание задачи.
- **Категория**: Категория задачи (например, Работа, Личное).
- **Срок выполнения**: Срок выполнения задачи в формате `YYYY-MM-DD`.
- **Приоритет**: Уровень приоритета задачи (низкий, средний, высокий).
- **Статус**: Текущий статус задачи (либо "Не выполнена", либо "Выполнена").

## Класс TaskManager

Класс `TaskManager` отвечает за загрузку, сохранение и управление задачами в файле JSON. Он предоставляет следующие
методы:

- `load_tasks()`: Загружает задачи из файла `tasks.json`.
- `save_tasks()`: Сохраняет текущий список задач в файл `tasks.json`.
- `add_task()`: Добавляет новую задачу в список.
- `get_task_by_id()`: Получает задачу по ее ID.
- `show_tasks()`: Отображает список задач.

## Класс Task

Класс `Task` представляет отдельную задачу и предоставляет методы для:

- `mark_as_done()`: Отметить задачу как выполненную.
- `edit()`: Редактировать данные задачи (название, описание, категория, срок выполнения, приоритет).
- `to_dict()`: Преобразует задачу в словарь (для сохранения в JSON).
- `from_dict()`: Создает задачу из словаря.

## Класс MenuHandler

Класс `MenuHandler` отвечает за взаимодействие с пользователем. Он отображает меню, обрабатывает выбор пользователя и
вызывает соответствующие методы из класса `TaskManager`.

## Пример взаимодействия

```
Главное меню:
1. Просмотр задач
2. Добавить задачу
3. Изменить задачу
4. Удалить задачу
5. Поиск задач
6. Выход

Выберите действие: 2

Добавление задачи:
Название задачи: Новый проект
Описание задачи: Завершить проект до конца месяца
Категория задачи: Работа
Срок выполнения (гггг-мм-дд): 2024-12-15
Приоритет задачи (низкий, средний, высокий): высокий

Задача добавлена.
Нажмите Enter для возврата в меню.
```