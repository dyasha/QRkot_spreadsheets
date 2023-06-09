# __QRKot API__
## API для благотворительного фонда поддержки котиков QRKot. Фонд собирает пожертвования на различные целевые проекты, связанные с поддержкой кошачьей популяции.

### __Проекты__
В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.
### __Пожертвования__
Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

## __Установка__
Склонируйте проект на Ваш компьютер
   ```
   git clone https://github.com/Dyasha/cat_charity_fund.git
   ```
Перейдите в папку с проектом
   ```
   cd cat_charity_fund
   ```
Активируйте виртуальное окружение
   ```
   python3 -m venv venv
   ```
   ```
   source venv/bin/activate
   ```
Обновите менеджер пакетов (pip)
   ```
   pip3 install --upgrade pip
   ```
Установите необходимые зависимости
   ```
   pip3 install -r requirements.txt
   ```
## __Использование__
Для запуска проекта выполните команду
```
uvicorn app.main:app --reload
```
## __Эндпоинты__

### __Получение списка всех проектов__
#### __GET /charity_project/__
#### Возвращает список всех проектов, включая требуемые и уже внесенные суммы.

```
[
    {
        "name": "Проект 1",
        "description": "Описание проекта 1",
        "full_amount": 1000,
        "id": 2,
        "invested_amount": 500,
        "fully_invested": false,
        "create_date": "2023-03-21T12:00:00",
        "close_date": "2023-03-21T12:00:00"
    },
    {
        "name": "Проект 2",
        "description": "Описание проекта 2",
        "full_amount": 500,
        "id": 2,
        "invested_amount": 500,
        "fully_invested": true,
        "create_date": "2023-03-21T12:00:00",
        "close_date": "2023-03-21T12:00:00"
    }
]

```

### __Создание нового проекта__
#### __POST /charity_project/__
#### Создает новый проект в базе данных. Доступно только суперпользователям.
Запрос
```
{
  "name": "New Project",
  "description": "Description for project",
  "full_amount": 100000
}
```
Ответ
```
{
  "name": "New Project",
  "description": "Description for project",
  "full_amount": 100000,
  "id": 14,
  "invested_amount": 0,
  "fully_invested": false,
  "create_date": "2023-03-21T17:25:38.909499"
}
```

### __С остальными эндпоинтами можно ознакомиться по адресу '/docs'__

## __Автор__
###  [Береснев Владислав](https://github.com/dyasha)