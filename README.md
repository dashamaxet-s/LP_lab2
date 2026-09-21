# Concurrency Benchmark: threading vs multiprocessing vs asyncio

Сравнение трёх моделей конкурентности Python на двух типах нагрузки:
- **CPU-bound:** подсчёт простых чисел.
- **I/O-bound:** HTTP-запросы к локальному мок-серверу.

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone git@github.com:dashamaxet-s/LP_lab2.git
   cd LP_lab2
   ```

2. Создайте и активируйте виртуальное окружение:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate      # Windows
   source .venv/bin/activate   # Mac/Linux
   ```

3. Установите пакет и зависимости:
   ```bash
   pip install -e .
   pip install -e ".[dev]"
   pip install -e ".[io]"
   ```

## Запуск мок-сервера

Для I/O-нагрузки нужен локальный мок-сервер. Запустите его в **отдельном терминале**:

```bash
python -m concurrency.mock_server
```

Сервер будет слушать `http://127.0.0.1:8000`. Не закрывайте этот терминал.

## Запуск бенчмарков

### CPU-нагрузка

```bash
concurrency --load cpu --mode threading --n 500000
concurrency --load cpu --mode multiprocessing --n 500000
concurrency --load cpu --mode asyncio --n 500000
```

### I/O-нагрузка

```bash
concurrency --load io --mode threading --m 50
concurrency --load io --mode multiprocessing --m 50
concurrency --load io --mode asyncio --m 20
```

### Параметры CLI

| Опция | Описание |
| :--- | :--- |
| `--load {cpu,io}` | Тип нагрузки (обязательный) |
| `--mode {threading,multiprocessing,asyncio}` | Модель конкурентности (обязательный) |
| `--n N` | Параметр для CPU: до какого числа считать простые (по умолчанию 10000) |
| `--m M` | Параметр для I/O: количество HTTP-запросов (по умолчанию 100) |
| `--workers W` | Количество рабочих в пуле (по умолчанию 4) |

## Проверка качества

```bash
mypy src
ruff check src
pytest
```

## Результаты

Смотрите `docs/report.md` с таблицами и объяснением результатов через GIL.