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
        url = ['https://market.yandex.ru/product--vykliuchatel-2kh1-poliusnyi-aqara-qbkg03lm-belyi/449231070?skuId=449231070&sku=449231070&show-uid=16476000163530332631706007&offerid=-Mn86HHkbPqRrIxKHZvRoA&cpc=aGzBg-jTvyKyFJjiKwsBudgWvk7hXGZ3KI9Tvj5PE8N-143_xGG2j10kOaCm2yHzHEo-GU6vy-mV7q_9lbsyDXl8ZD4dybAQxlWv4p2CTpQbQziTBMRS37cse0-_gYPWz04DrdPVfqutqklB3yitIowIFijDRpuVqLQQ6G3c8ApULeLvk7RE1w%2C%2C',
               'https://market.yandex.ru/product--315125-mashina-metall-skoda-kodiaq-matovyi-12-sm-dveri-bagazh-iner-seryi-kor-tekhnopark-v-k-2-36sht/1443675530?skuId=101453691114&sku=101453691114&show-uid=16476000163480221681006002&offerid=Wmw_wDoM-a8dxH2VbTBszw&cpc=fgJnssiBjSqJryLa4On9_QAskUQ73U0WdRGDZkl6KHS37t3-IGVztfQLviQFdfWXfplhIQJP5yd6ZqbmBlwtnZtjhMM6x8TQ2I51lW7iTvMxIv8DUJrVTNjvuVHIreCGD9Wrl4Qme-LPyy1B3zWi-ITzoSZ7KZ6ugDLCAtACoxN8ozXlqNS6YqqLKO6o549-', 
               'https://market.yandex.ru/product--noutbuk-honor-magicbook-x15-bbr-wai9-53011ugc-intel-core-i3-10110u-2-1-ghz-8192mb-256gb-ssd-intel-uhd-graphics-wi-fi-bluetooth-cam-15-6-1920x1080-windows-10-home-64-bit/938272877?skuId=101298460398&sku=101298460398&show-uid=16476000163540359491306008&offerid=aFCR5yPqnzL2rIgZV8K0fg&cpc=EcmkqLYmEul5Zvq3WzshJ3n6JcDnVzyM_FEMWR4pntvSn5TRqpy8uNiFPysQJdxBqg5Ng1vCceIVPk4EkSupGGzRMJdKmhDAXJycWJwGmZEAj8cDlhZ-KVcJXutb8_rNh-q-_exttx4C0A-p6YzQhmLPsa8zoZUhXkowccxlz65E_n-m-bOMIu2UKU4KvApm',
               'https://market.yandex.ru/product--elektrosamokat-xiaomi-mijia-m365-pro-black/394271125?skuId=100589021910&sku=100589021910&show-uid=16476000163680600522406022&offerid=apbIhkQmTeMbCg21Nucf_g&cpc=Lvgmn-ALRukp0HFrP6RNKrEXCaTuCWhJgnUkIfxXQrJUbIE21pg2ZkIYN8fZ_9IaqXFWzQrsibcGBC2CXwRsyNwPV7ba-eNhcO9tEW8bMzYN4ePJVNOnsecWF4yfzRsjXnqvaOLnHQ9atMmRsr_1E23dR9_slZR4sbn2ZAd2wBVIGjKA0MDWmSiujALGUTQ_', 
               'https://market.yandex.ru/product--bagazhnik-na-kryshu-lux-hunter-l54-r-dlia-skoda-kodiaq-vnedorozhnik-2017-klassicheskie-reilingi-na-reilingi-s-prosvetom-seryi/975241231?skuId=101341307090&sku=101341307090&show-uid=16476000163690621623806023&offerid=0ONs5KyDpqaJqcRh_MvkXA&cpc=QfGMbFPK_z7AVf16fUuJ443JAC2LJDOmD7FXOmxrbTH7JqPwhHiVNe5DQxSgwfiJsP6pp3JX_y1i2zXY3oqB90eNghL6cA2xGzBb7JooPAvSllKu0IslpvjgDs6WBt00s_AVUYjcd4rvtSIA2kzT5WFm8_NtJdcx1d5J1_7SzuVzgEjHZqAAHVHoCYN5-J3q', 
               'https://market.yandex.ru/product--kraskopult-aerograf-quattro-elementi-770-858/1973626371?skuId=1973626371&sku=1973626371&show-uid=16476000163620491774706016&offerid=edZAq_7wFbBbs35-xnOLXw&cpc=1xlXDsgyLd2vguveegfgCiOphaOBH06CXgSl6PXBMUCmOjUo2pulI_aTAKzLrFvnnmxPqOmf5zJY-uvSCQxwGD6UkcYfmmOqYJsB9E0SH12gcYbPkhsBDi_4TJrsE7Wsh-t10iDl4ZKDzL9G72mfhMpzOx0c82pkdQRJIUuXHm5G_yHsdG_Qbw%2C%2C', 
               'https://market.yandex.ru/product--futbolka-dream-shirts-ne-smei-chitat/902907026?skuId=101262684767&sku=101262684767&show-uid=16476000163490268007106003&offerid=Po70l0V286SfgMhEE4bGTg&cpc=_jZkicUufiYPJ-MGE7luZmDjJZYwNNf1jt-unEoKBGOSK5FiqJoEibewYLJ8GiFIRohldGAvTvRVpFDGHhRKAWAK1RIqF3UjqZIZ5o-Vxa6-3q1DsNoQknf6CiEitLwoBivd628v2y1PqOBB5kuKm5GS2OVonWt2hLDHRx93ryLcaJ_XkK1E7g%2C%2C',
               'https://market.yandex.ru/product--noutbuk-huawei-matebook-d-15-bob-wai9-53011uwy-intel-core-i3-10110u-2-1ghz-8192mb-256gb-ssd-no-odd-intel-uhd-graphics-wi-fi-bluetooth-cam-15-6-1920x1080-windows-10-64-bit/976588789?skuId=101343010734&sku=101343010734&show-uid=16476000163590446928606013&offerid=iGV6xMrfsOwKFAKuWXGRFg&cpc=jMwDQ_EDSjEDbrLYVLPkaHCJQU5waoN1eeXJJi_XO9gOkxjiuN89rZ9HALzViEpiGqDPtkH8msm-3nLedXhAecyzmYlG4q3VaYTp8p5VBYl_JZ9sjoWxHR4JwwB1Co_obNcPvTb2L1AVVOJLEqJMb6MaLSZ5ArWn2zWfID16baSy6cLX3qQPzUakG3_cw5OH',
               'https://market.yandex.ru/product--elektrobigudi-babyliss-bab3031e-chernyi/417035228?skuId=100607779991&sku=100607779991&show-uid=16476000163710664549006025&offerid=8Rf3N_kehfS6jMAOIPe9Pg&cpc=zTaFGz4VgPjEDV7GBUcMMl-P-6MHPSNfUxQZH4psxJB0lJF6hyHU5PBqo7lNp2vvUNRgF5WdZNKQnpVjDRxuJVX3UFCiieQf-WMq-fpbsCh9-v1-5nFOl82B8PADSfsSxBZOrGK0KAzwBo6HAqVRP8mxZusilqhBP02HYRa19RbbB6yk_1Pg6Q%2C%2C',
               'https://market.yandex.ru/product--krossovki-baden-muzhskie-letnie-razmer-43-tsvet-sinii-artikul-vc001-033/1488972336?skuId=101525746529&sku=101525746529&show-uid=16476000163510296188906005&offerid=puYsIqHnUy4F7n3-VtX71w&cpc=AQRv-YTpmhDTDRVxc5g-HMTnrWE-tQ52pc057Pk1MyT_Xe6iEEAvH-pEWby-7wYl50He5DgNkueLMeUbSe2TTR7p45wfuALqY9Sd3EqYYV1dqaj540GQI2eyLD5wYWstKvj1WaUa4bhlYgBI6isK1tWWnJg48pS6ANlrbTqBQCnXaaqaoeRYOMy1X1BbqUdY']

        """ for z in range(1, 10):        
            for i in range(len(url)):
                 Link.objects.create(user_id=2, link=url[i])
            print("------------------") """
        def create_driver():
            options = Options()
            options.add_argument(f"user-data-dir={BASE_DIR}/Market_Parser")
            options.add_argument(
                "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
            """ options.add_argument("--headless")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--v=99")
            options.add_argument("--no-sandbox") """
            driver = webdriver.Chrome(executable_path='/home/falsehuman/web-whats-sendmessage/chromedriver', chrome_options=options)
            return driver

        def parser_yandex_market(link):
            driver = create_driver()
            driver.get(link)
            time.sleep(10)
            try:
                price = (driver.find_element_by_class_name(DIV_CLASS))
                price = (price.text).split('\n')
                pars_price =price[0].split(' ₽')[0].replace(' ', '')
                driver.quit()
                return pars_price
            except Exception as e:
                print(f'Ошибка парсинга {e}')
                driver.quit()
                return f'error {e}'

        links = Link.objects.all()

        print('Основа')
        for obj in links:
            #print(parser_yandex_market(obj.link))
            email = User.objects.get(username=obj.user).email
            quetstion_func = parser_yandex_market(obj.link)
            if 'error' in quetstion_func:
                print(quetstion_func)
                #subject, message = "Ошибка парсинга", f"Ошибка при парсинге ссылки: {obj.link} \n Лог ошибки {quetstion_func}"
                #send_mail( subject,message, EMAIL_HOST_USER, [EMAIL_HOST_USER], fail_silently=False,)
            else:
                last_price = PriceLink.objects.filter(price_link_id=obj.id)
                if len(last_price) != 0:
                    if (int(last_price[len(last_price)-1].price) != int(quetstion_func)) == True:
                        #subject, message = "Изменение цены", f"Изменилась цена товара по ссылке: {obj.link}\nБыла {last_price[len(last_price)-1].price}₽, стала {pars_price}₽"
                        #send_mail( subject,message, EMAIL_HOST_USER, [email], fail_silently=False,)
                        PriceLink.objects.create(price_link_id=obj.id, price=quetstion_func)
                else:
                    #subject, message = "Добавление товара на парсинг", f"Добавлен товар на парсинг: {obj.link}\nТекущая цена {pars_price}₽"
                    #send_mail( subject,message, EMAIL_HOST_USER, [email], fail_silently=False,)
                    PriceLink.objects.create(price_link_id=obj.id, price=quetstion_func)


        print('Аналогичные товары')
        links = AnalogLink.objects.all()
        for obj in links:
            #print(parser_yandex_market(obj.link))
            quetstion_func = parser_yandex_market(obj.link)
            if 'error' in quetstion_func:
                print(quetstion_func)
                #subject, message = "Ошибка парсинга", f"Ошибка при парсинге ссылки: {obj.link} \n Лог ошибки {quetstion_func}"
                #send_mail( subject,message, EMAIL_HOST_USER, [EMAIL_HOST_USER], fail_silently=False,)
            else:
                last_price = AnalogLinkPrice.objects.filter(analog_link_price_id=obj.id)
                if len(last_price) != 0:
                    if (int(last_price[len(last_price)-1].analog_price) != int(quetstion_func)) == True:
                        #subject, message = "Изменение цены", f"Изменилась цена товара по ссылке: {obj.link}\nБыла {last_price[len(last_price)-1].price}₽, стала {pars_price}₽"
                        #send_mail( subject,message, EMAIL_HOST_USER, [email], fail_silently=False,)
                        AnalogLinkPrice.objects.create(analog_link_price_id=obj.id, analog_price=quetstion_func)
                else:
                    #subject, message = "Добавление товара на парсинг", f"Добавлен товар на парсинг: {obj.link}\nТекущая цена {pars_price}₽"
                    #send_mail( subject,message, EMAIL_HOST_USER, [email], fail_silently=False,)
                    AnalogLinkPrice.objects.create(analog_link_price_id=obj.id, analog_price=quetstion_func)
        self.stdout.write("Закончен процесс парсинга")
