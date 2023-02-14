# django_stripe_test
### Описание
Тестовое задание по интеграции платежного сервиса [Stripe](https://stripe.com/en-gb) в проект Django    
Ссылка на тестовый сайт - http://vershinin86.pythonanywhere.com/

## Установка
- python 3.9-3.11
- клонируйте репозиторий, используя команду в терминале `git clone https://github.com/alexeyvershinin/django_stripe_test.git` или скачайте архив по [ссылке](https://github.com/alexeyvershinin/django_stripe_test/archive/refs/heads/master.zip)   
- перейдите в папку с проектом и создайте виртуальное окружение командой `python -m venv env`   
- используя команду `cd .\env\Scripts\` перейдите в каталог с установленным ранее виртуальным окружением и запустите виртуальное окружение командой `.\activate`
- установите необходимые зависимости `pip install -r requirements.txt`
- создайте суперпользователя командой `python manage.py createsuperuser`
- запустите сервер `python manage.py runserver`

Данные тестовых карт оплаты Stripe Вы найдете по данной [ссылке](https://stripe.com/docs/testing)
