import requests


url = "https://www.wildberries.ru"


# inicialize session
with requests.Session() as se:
    se.headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
            "(KHTML, like Gecko) Chrome/91.0.4472.114"
            "Safari/537.36"
        ),
        "accept-encoding": "gzip, deflate, br",
        "accept": "*/*",
    }

    def main():
        # if you using my work for freelance,
        # i will be glad to see a pull request,
        # with cod, to make it better,
        # because i_m only student
        sub_url = get_category(
            url, 'li', 'a',
            class_=('menu-burger__main-list-item j-menu-main-item',)
        )
        sub_sub_url = get_category(
            sub_url, 'ul', 'a',
            class_=('menu-catalog__list-2', '')
        )
        while sub_sub_url:
            sub_sub_url = get_category(
                sub_sub_url, 'li', 'ul', 'a',
                class_=('selected hasnochild', '', '')
            )


if __name__ == '__main__':
    from choose_category import get_category
    main()
