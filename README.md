# django_sprint4
Проект был создан с использованием [uv](https://docs.astral.sh/uv/) и [just](https://github.com/casey/just).

## Доступные команды в just
- `just run` - Запустить проект
- `just migrate` - Создать и проделать миграции
- `just loaddata {файл}` - Загрузить микстуры из файла
- `just test` - Запустить тесты

## Запуск проекта
### `uv` + `just` (Рекомендуется)
1) Установить [`uv`](https://github.com/casey/just) и [`just`](https://github.com/casey/just)
2) `just migrate`
3) `just loaddata db.json`
4) `just run`

### Вручную
1) Создать и открыть виртуальное окружение
2) Установить в него пакеты из requirements.txt
3) Перейти в папку blogicum
4) Создать и произвести миграции
5) Загрузить микстуры из файла db.json
6) `python manage.py runserver`