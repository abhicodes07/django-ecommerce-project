# 🌿 Django E-commerce Project

A Django-based e-commerce application with product browsing and typical commerce workflows (catalog, cart/checkout style flows, and admin management). This repository contains the backend (and any included templates/static assets) needed to run the project locally for development and testing.

## 🚀 Getting Started

<details>
<summary> <b> Clone the repository </b> </summary>
<br>

```bash
git clone https://github.com/abhicodes07/django-ecommerce-project.git
cd django-ecommerce-project
```

</details>

<details>
<summary><b>Create and activate a virtual environment</b></summary>
<br>

**macOS / Linux**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

</details>

<details>
<summary><b>Install dependencies</b></summary>
<br>

If you have a `requirements.txt`:

```bash
pip install -r requirements.txt
```

If you use **Poetry** or **uv**, install with your tool of choice instead.

</details>

<details>
<summary><b>Configure environment variables</b></summary>
<br>

This project may require environment variables (e.g., `SECRET_KEY`, database settings, debug flags).

Create a `.env` file (optional but recommended) in the project root, for example:

```bash
# .env (example)
DJANGO_SECRET_KEY=replace-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

If your project uses `python-decouple` or `django-environ`, ensure your settings load `.env` accordingly.

> Note: If your project does **not** use `.env`, configure values directly in your Django `settings.py` (development only) or via shell environment variables.

</details>

<details>
<summary><b>Apply migrations</b></summary>
<br>

```bash
python manage.py makemigrations
python manage.py migrate
```

</details>

<details>
<summary><b>Create an admin user</b></summary>
<br>

```bash
python manage.py createsuperuser
```

</details>

<details>
<summary> <b> Run the development server</b> </summary>
<br>

```bash
python manage.py runserver
```

Visit:

- App: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/
</details>

## 🐚 Common Django Commands

```bash
# start server
python manage.py runserver

# create migrations and migrate
python manage.py makemigrations
python manage.py migrate

# create super user
python manage.py createsuperuser

# start tailwind server
python manage.py tailwind start

# build tailwind style
python manage.py tailwind build

# collect static
python manage.py collectstatic
```

## 🧪 Testing

<details>
<summary><b>Install test dependencies</b></summary>
<br>
Add these to your environment (or your requirements file):

```bash
pip install pytest pytest-django coverage factory-boy
```

Optional but useful:

```bash
pip install pytest-cov
```

</details>

<details>
<summary><b>Configure `pytest` (recommended)</b></summary>
<br>

Create a `pytest.ini` in the repository root:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = <your_project_name>.settings
python_files = tests.py test_*.py *_tests.py
addopts = -ra
```

Replace:

- `<your_project_name>.settings` with your actual Django settings module (for example `config.settings` or `ecommerce.settings`).

> If you already have a settings module split (e.g., `settings/dev.py`, `settings/test.py`), point `DJANGO_SETTINGS_MODULE` to the test settings module.

</details>

<details>
<summary><b>Run tests</b></summary>
<br>

```bash
pytest
```

To run a specific test file:

```bash
pytest path/to/test_file.py
```

To run tests matching a keyword:

```bash
pytest -k "checkout"
```

</details>

<details>
<summary><b>Run tests with coverage</b></summary>
<br>

Run coverage against your Django project/apps:

```bash
coverage run -m pytest
```

Generate an HTML report:

```bash
coverage html
```

this creates a `htmlcov` directory containing the `index.html` as a result for the tests.

- Accessing `coverage` HTML output (linux):

```bash
# in root dir
cd htmlcov && explorer.exe index.html
```

</details>

## 📂 Project Structure

```

./
├── .czrc
├── .gitignore
├── .python-version
├── pyproject.toml
├── README.md
├── requirements.txt      # dependencies
├── setup.cfg
├── src/
│   ├── .coveragerc       # coverage config
│   ├── apps/             # site applications
│   │   ├── __init__.py
│   │   ├── account/
│   │   ├── basket/
│   │   ├── orders/
│   │   ├── payment/
│   │   └── store/
│   ├── conftest.py       # pytest fixtures
│   ├── core/             # core files
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── debug.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── manage.py*
│   ├── payments_sdk.prp  # worldline properties file
│   ├── pytest.ini        # pytest global config
│   ├── static/           # static files
│   ├── templates/        # global templates
│   └── tests/            # global tests/factories
└── uv.lock               # lock file
```

---

 <p align="center"><img alt="Static Badge" src="https://img.shields.io/badge/LICENSE-MIT-cba6f7?style=for-the-badge&labelColor=%23222436"></p>
