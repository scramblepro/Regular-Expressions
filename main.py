import csv
import re
from pprint import pprint

# Читаем адресную книгу в формате CSV в список contacts_list
with open("phonebook_raw.csv", encoding="utf-8") as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Функция для разделения ФИО на отдельные поля
def split_fullname(fullname):
    parts = fullname.split()
    if len(parts) == 3:
        return parts
    elif len(parts) == 2:
        return parts + ['']
    elif len(parts) == 1:
        return parts + ['', '']
    else:
        return ['', '', '']

# Функция для приведения телефона к единому формату
def format_phone(phone):
    pattern = re.compile(r"(\+7|8)?\s*\(?(\d{3})\)?[\s-]?(\d{3})[\s-]?(\d{2})[\s-]?(\d{2})(\s*доб\.\s*(\d+))?")
    formatted_phone = pattern.sub(r"+7(\2)\3-\4-\5\6\7", phone)
    return formatted_phone

# Преобразование данных и объединение записей
contacts_dict = {}
header = contacts_list[0]

for contact in contacts_list[1:]:
    lastname, firstname, surname = split_fullname(" ".join(contact[:3]))
    organization = contact[3]
    position = contact[4]
    phone = format_phone(contact[5])
    email = contact[6]

    key = (lastname, firstname)
    
    if key not in contacts_dict:
        contacts_dict[key] = [lastname, firstname, surname, organization, position, phone, email]
    else:
        existing_contact = contacts_dict[key]
        for i, value in enumerate([surname, organization, position, phone, email]):
            if value and not existing_contact[i+2]:
                existing_contact[i+2] = value

# Преобразование словаря обратно в список
contacts_list = [header] + list(contacts_dict.values())

# Сохранение получившихся данных в другой файл
with open("phonebook.csv", "w", encoding="utf-8", newline='') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)

pprint(contacts_list)
