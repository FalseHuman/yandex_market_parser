import os
from django.core.management.base import BaseCommand
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from core.settings import BASE_DIR, DIV_CLASS, EMAIL_HOST_USER
from ...models import *
from django.contrib.auth.models import User
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Парсер цены товара с Яндекс.Маркета'

    def handle(self, *args, **kwargs):
        self.stdout.write("Начат процесс парсинга")
        def create_driver():
            options = Options()
            #options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
            options.add_argument(f"user-data-dir={BASE_DIR}/Market_Parser")
            options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
            options.add_argument("--headless")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--v=99")
            options.add_argument("--no-sandbox")
            driver = webdriver.Chrome(chrome_options=options)
            return driver

        def parser_yandex_market(link):
            driver = create_driver()
            driver.get(link)
            time.sleep(20)
            try:
                price = (driver.find_element_by_class_name(DIV_CLASS))
                price = (price.text).split('\n')
                arr_price = []
                print(price)
                for i in range(len(price)):
                    if(' ₽'in price[i]):
                        arr_price.append(int(price[i].replace(' ', '').replace('₽', '')))
                    elif ' ₽'in price[i]:
                        arr_price.append(int(price[i].replace(' ', '').replace('₽', '')))#int(price[i].split(' ₽')[0].replace(' ', '')))

                print(arr_price)
                pars_price = min(arr_price)
                driver.quit()
                return pars_price
            except Exception as e:
                print(f'Ошибка парсинга {e}')
                subject, message = "Ошибка парсинга", f"Ошибка при парсинге ссылки: {link} \n Лог ошибки {e}"
                send_mail( subject,message, EMAIL_HOST_USER, [EMAIL_HOST_USER], fail_silently=False,)
                driver.quit()
                return 'error'
                    
                    
        links = Link.objects.all()

        print('Основа')
        for obj in links:
            #print(parser_yandex_market(obj.link))
            email = User.objects.get(username=obj.user).email
            quetstion_func = parser_yandex_market(obj.link)
            """ if 'error' in quetstion_func:
                print(quetstion_func)
                subject, message = "Ошибка парсинга", f"Ошибка при парсинге ссылки: {obj.link} \n Лог ошибки {quetstion_func}"
                send_mail( subject,message, EMAIL_HOST_USER, [EMAIL_HOST_USER], fail_silently=False,)
            else: """
            if quetstion_func != 'error':
                last_price = PriceLink.objects.filter(price_link_id=obj.id)
                if len(last_price) != 0:
                    if (int(last_price[len(last_price)-1].price) != int(quetstion_func)) == True:
                        subject, message = "Изменение цены", f"Изменилась цена товара по ссылке: {obj.link}\nБыла {last_price[len(last_price)-1].price}₽, стала {quetstion_func}₽"
                        send_mail( subject,message, EMAIL_HOST_USER, [email], fail_silently=False,)
                        PriceLink.objects.create(price_link_id=obj.id, price=quetstion_func)
                else:
                    subject, message = "Добавление товара на парсинг", f"Добавлен товар на парсинг: {obj.link}\nТекущая цена {quetstion_func}₽"
                    send_mail( subject,message, EMAIL_HOST_USER, [email], fail_silently=False,)
                    PriceLink.objects.create(price_link_id=obj.id, price=quetstion_func)


        print('Аналогичные товары')
        links = AnalogLink.objects.all()
        for obj in links:
            #print(parser_yandex_market(obj.link))
            quetstion_func = parser_yandex_market(obj.link)
            """ if 'error' in quetstion_func:
                print(quetstion_func)
                subject, message = "Ошибка парсинга", f"Ошибка при парсинге ссылки: {obj.link} \n Лог ошибки {quetstion_func}"
                send_mail( subject,message, EMAIL_HOST_USER, [EMAIL_HOST_USER], fail_silently=False,)
            else:"""
            if quetstion_func != 'error':
                last_price = AnalogLinkPrice.objects.filter(analog_link_price_id=obj.id)
                if len(last_price) != 0:
                    if (int(last_price[len(last_price)-1].analog_price) != int(quetstion_func)) == True:
                        subject, message = "Изменение цены", f"Изменилась цена товара по ссылке: {obj.link}\nБыла {last_price[len(last_price)-1].price}₽, стала {quetstion_func}₽"
                        send_mail( subject,message, EMAIL_HOST_USER, [email], fail_silently=False,)
                        AnalogLinkPrice.objects.create(analog_link_price_id=obj.id, analog_price=quetstion_func)
                else:
                    subject, message = "Добавление товара на парсинг", f"Добавлен товар на парсинг: {obj.link}\nТекущая цена {quetstion_func}₽"
                    send_mail( subject,message, EMAIL_HOST_USER, [email], fail_silently=False,)
                    AnalogLinkPrice.objects.create(analog_link_price_id=obj.id, analog_price=quetstion_func)


                """ price = (driver.find_element_by_class_name(DIV_CLASS))
                price = (price.text).split('\n')
                arr_price = []
                print(price)
                for i in range(len(price)):
                    if(' ₽'in price[i]):
                        arr_price.append(int(price[i].replace(' ', '').replace('₽', '')))

                print(min(arr_price))
                pars_price = min(arr_price) """
                """ if len(price) > 2:          
                    pars_price_1 = price[0].split(' ₽')[0].replace(' ', '')
                    pars_price_2 = price[2].split(' ₽')[0].replace(' ', '')
                    if pars_price_2 > pars_price_1:
                        pars_price = pars_price_2
                    else:
                        pars_price = pars_price_1
                else:
                    pars_price =price[0].split(' ₽')[0].replace(' ', '') """

                    #print(pars_price)
                #print(int(pars_price))
                """ last_price = PriceLink.objects.filter(price_link_id=obj.id)
                if len(last_price) != 0:
                    if (int(last_price[len(last_price)-1].price) != int(pars_price)) == True:
                        subject, message = "Изменение цены", f"Изменилась цена товара по ссылке: {obj.link}\nБыла {last_price[len(last_price)-1].price}₽, стала {pars_price}₽"
                        send_mail( subject,message, EMAIL_HOST_USER, [email], fail_silently=False,)
                        PriceLink.objects.create(price_link_id=obj.id, price=int(pars_price))
                else:
                    subject, message = "Добавление товара на парсинг", f"Добавлен товар на парсинг: {obj.link}\nТекущая цена {pars_price}₽"
                    send_mail( subject,message, EMAIL_HOST_USER, [email], fail_silently=False,)
                    PriceLink.objects.create(price_link_id=obj.id, price=int(pars_price))
            except Exception as e:
                    print(f'Ошибка парсинга {e}')
                    subject, message = "Ошибка парсинга", f"Ошибка при парсинге ссылки: {obj.link} \n Лог ошибки {e}"
                    send_mail( subject,message, EMAIL_HOST_USER, [EMAIL_HOST_USER], fail_silently=False,) """
        self.stdout.write("Закончен процесс парсинга")