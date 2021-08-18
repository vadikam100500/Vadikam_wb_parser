from bs4 import BeautifulSoup

from parser import parser_main
from main import se


# for each of this category, you need rewrite separate logic
# it's only 5 categories from 26, that's why i'm lazy,
# and don't whant to write thems
# if it will be a real freelance order, of course i would add them
stop_category = ('Видеообзоры', 'Premium', 'Спорт', 'Бренды', 'Акции')

main_url = 'https://www.wildberries.ru'


def input_category_check(dict):
    input_category = input("\nВЫБЕРИТЕ КАТЕГОРИЮ: ").lower()
    # checking that user input category correctly
    while input_category not in dict:
        print("\nПроверьте верно ли вы ввели категорию")
        input_category = input(
            "\nВЫБЕРИТЕ КАТЕГОРИЮ СНОВА (без пробелов по бокам!): "
        ).lower()
    return input_category


def get_category(url, *args, **kwargs):
    # connect to main page
    resp = se.get(url)
    # get html
    category_page = BeautifulSoup(resp.content, 'html.parser')
    # find all categories
    categories = category_page.find_all(args[0], kwargs['class_'][0])
    count = len(kwargs['class_'])
    if count > 1:
        try:
            categories = categories[0].find_all(args[1], kwargs['class_'][1])
            if count > 2:
                categories = categories[0].find_all(args[2])
        except IndexError:
            pass
    category_dict = {}
    for category in categories:
        # getting each category
        if count > 1:
            category_name = category
        else:
            category_name = category.find(args[1])
        try:
            # getting href
            href = category_name.get('href')
            if count > 1:
                href = f'{main_url}{href}'
            text_name = category_name.get_text()
            # add category and href to dict
            category_dict[text_name.lower()] = href
            # show all categories for user
            if text_name not in stop_category:
                print(text_name)
        except AttributeError:
            # in some categories, wb give not need data
            pass
    if not category_dict:
        parser_main(url)
    else:
        input_category = input_category_check(category_dict)
        return category_dict[input_category]
