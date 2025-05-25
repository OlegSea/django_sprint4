set shell := ["powershell.exe", "-c"]
set working-directory := 'blogicum'

manage +something:
    uv run manage.py {{something}}

run:
    @just manage runserver

migrate:
    @just manage makemigrations
    @just manage migrate

loaddata file:
    @just manage loaddata {{file}}

[working-directory: '..']
test:
    uv run pytest

    