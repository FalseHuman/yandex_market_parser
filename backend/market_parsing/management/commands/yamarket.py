import os
from django.core.management.base import BaseCommand
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from core.settings import BASE_DIR, DIV_CLASS, EMAIL_HOST_USER
from ...models import Link, PriceLink
from django.contrib.auth.models import User
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Парсер цены товара с Яндекс.Маркета'

    def handle(self, *args, **kwargs):
        self.stdout.write("Начат процесс парсинга")
        def create_driver():
            options = Options()
            options.add_argument(f"user-data-dir=YOUR_PATH_PROFILE_CHROME")
            options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
            options.add_argument("--headless")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--v=99")
            options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(executable_path='YOUR_PATH_CHROMEDRIVER', chrome_options=options)
            return driver

        
        links = Link.objects.all()
        for obj in links:
            driver = create_driver()
            email = User.objects.get(username=obj.user).email
            driver.get(obj.link)
            time.sleep(10)

            try:
                price = (driver.find_element_by_class_name(DIV_CLASS))
                price = (price.text).split('\n') 
                #print(price)             
                pars_price =price[0].split(' ₽')[0].replace(' ', '')
                #print(int(pars_price))
                last_price = PriceLink.objects.filter(price_link_id=obj.id)
                if len(last_price) != 0:
                    if (int(last_price[len(last_price)-1].price) != int(pars_price)) == True:
                        subject, message = "Изменение цены", f"Изменилась цена товара по ссылке: {obj.link}\nБыла {last_price[len(last_price)-1].price}₽, стала {pars_price}₽"
                        send_mail( subject,message, EMAIL_HOST_USER, [email], fail_silently=False,)
                        PriceLink.objects.create(price_link_id=obj.id, price=pars_price)
                else:
                    subject, message = "Добавление товара на парсинг", f"Добавлен товар на парсинг: {obj.link}\nТекущая цена {pars_price}₽"
                    send_mail( subject,message, EMAIL_HOST_USER, [email], fail_silently=False,)
                    PriceLink.objects.create(price_link_id=obj.id, price=pars_price)
            except Exception as e:
                    print(f'Ошибка парсинга {e}')
                    subject, message = "Ошибка парсинга", f"Ошибка при парсинге ссылки: {obj.link} \n Лог ошибки {e}"
                    send_mail( subject,message, EMAIL_HOST_USER, [EMAIL_HOST_USER], fail_silently=False,)

            driver.quit()
        self.stdout.write("Закончен процесс парсинга")