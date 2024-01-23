import requests
from bs4 import BeautifulSoup

url = "https://nadezhdin2024.ru/addresses"

# Отправляем запрос на получение HTML-страницы
response = requests.get(url)

# Проверяем успешность запроса
if response.status_code == 200:
    # Создаем объект BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все элементы с классом 'adresses-page__region'
    region_elements = soup.find_all(class_='addresses-page__region')

    if region_elements:
        region_data_list = []

        for region_element in region_elements:
            progress_text_element = region_element.select_one('.progressbar__el__text')

            if progress_text_element:
                progress_text = progress_text_element.text.strip()
                # Берем только те строки где есть данные
                if progress_text != "Ждём данных от штаба":
                    region_data_list.append(progress_text)
        # Отрезаем слова "Собрано подписей:"
        list_number=[]
        for x in region_data_list:
            y = x[18:]
            list_number.append(y)
        # Отрезаем квоту там где это нужно
        list_clear_number=[]
        for x in list_number:
            if '/' in x:
                y = x.split('/')[0]
            else:
                y=x
            list_clear_number.append(int(y))
        # Считаем только по квотам
        clear_sum=0
        for x in list_clear_number:
            if x>2500:x=2500
            clear_sum+=x
        print(f"Всего подписей {sum(list_clear_number)}")
        print(f"Учитывая квоты {clear_sum}")
    else:
        print("Элементы не найдены.")
else:
    print(f"Ошибка при запросе: {response.status_code}")
