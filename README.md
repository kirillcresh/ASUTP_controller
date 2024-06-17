# ASUTP_controller

## Work with Poetry
```sh
1. pip install poetry
2. деактивируем рабочую виртуальную среду deactivate
3. активируем poetry среду командой poetry shell
4. устанавливаем зависимости poetry install
5. добавляем новый интерпретатор (poetry environment) путь по умолчанию:
"C:\Users\AppData\Local\pypoetry\Cache\virtualenvs\название_текущего_проекта\Scripts\python.exe"
6. меняем интерпретатор в конфигурации edit configurations
7. для добавления новой зависимости poetry add <package>
8. чтобы зависимость была у всех разработчиков пишем poetry lock
```

## Alembic миграции

### Обновление состояния БД до последней миграции
```sh
$ alembic upgrade head
```

### Создание новой миграции

Именованная миграция:
```sh
$ alembic revision --autogenerate -m "НАЗВАНИЕ МИГРАЦИИ"
```

Миграция без названия:
```sh
$ alembic revision --autogenerate
```
