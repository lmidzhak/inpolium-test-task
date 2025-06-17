# 📘 Inpolium Test Task – FastAPI App

Це FastAPI застосунок для управління постами, темами та коментарями. Підтримується створення, перегляд, пошук за ідентифікатором, оновлення та видалення постів з відповідним видаленням коментарів до цих постів.

## 🛠 Встановлення

### 1. Клонування репозиторію

```bash
git clone https://github.com/lmidzhak/inpolium-test-task.git
cd inpolium-test-task
```

### 2. Створення та активація віртуального середовища
```bash
python -m venv venv
```
```bash
source venv/bin/activate   # Linux/macOS
```
```bash
venv\Scripts\activate      # Windows
```
### 3. Встановлення залежностей
```bash
pip install -r requirements.txt
```
### 4. Налаштування
Створи файл .env у корені проєкту зі змінною EXAMPLE_TOKEN:
```ini
EXAMPLE_TOKEN="your-secret-token"
```
### 5. Міграції (Alembic)
- ініціалізуй alembic
```bash
alembic init alembic
```
- згенеруй міграцію:
```bash
alembic revision --autogenerate -m "Initial migration"
```
- застосуй міграцію
```bash
alembic upgrade head
```
### 6. Запуск FastAPI застосунку
```bash
uvicorn main:app --reload
```
Після запуску буде доступна документація:

Swagger UI: http://127.0.0.1:8000/docs