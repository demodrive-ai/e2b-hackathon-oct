### Installation

Setting up the dev environment.

```bash
poetry config virtualenvs.in-project true
poetry install
cp env.example .env
```

To start the server

```bash
poetry run python blogchecker/manage.py runserver
```

To test E2B connection.

```bash
poetry run e2b_test.py
```
