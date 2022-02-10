import requests


def find_businesses(ll, spn, request, locale="ru_RU"):
    search_api_server = "https://search-maps.yandex.ru/v1/"
    search_params = {
        "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
        "text": request,
        "lang": locale,
        "ll": ll,
        "spn": spn,
        "type": "biz"
    }

    response = requests.get(search_api_server, params=search_params)
    if not response:
        raise RuntimeError(
            f"""Ошибка выполнения запроса: {search_api_server}
            Http статус: {response.status_code} ({response.reason})""")

    json_response = response.json()
    return json_response["features"]


def find_business(ll, spn, request, locale="ru_RU"):
    orgs = find_businesses(ll, spn, request, locale="ru_RU")
    if len(orgs):
        return orgs[0]
