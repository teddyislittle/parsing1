import requests
from bs4 import BeautifulSoup
import lxml
import json

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0"
}
# СПИСОК ПОД ССЫЛКИ
fest_links_list = []
for i  in range(0, 24, 24):
    url = f"https://www.skiddle.com/festivals/search/?ajaxing=1&sort=0&fest_name=festival%20finder&from_date=&to_date=&maxprice=500&o={i}&bannertitle=May"

    req = requests.get(url=url, headers=headers)
    json_data = json.loads(req.text)
    html_response = json_data["html"]

    with open(f"data/index_{i}.html", "w") as file:
        file.write(html_response)

    with open(f"data/index_{i}.html") as file:
        src = file.read()

    soup = BeautifulSoup(src, "lxml")
    cards = soup.find_all("a", class_="card-details-link")

    for item in cards:
        fest_links = "https://www.skiddle.com" + item.get("href")
        fest_links_list.append(fest_links)

# ПЕРЕХОД И СБОР ИНФОРМАЦИИ
count = 0
fest_list_result = []
for url in fest_links_list:
    count += 1


    req = requests.get(url=url, headers=headers)

    try:
        soup = BeautifulSoup(req.text, "lxml")
        fest_info_box = soup.find("div", class_="MuiBox-root")
        fest_name = fest_info_box.find("h1").text.strip()

        fest_date_info = soup.find("div", class_="MuiGrid-grid-xs-11")
        fest_date = fest_date_info.find("span").text.strip() + fest_date_info.find("span").next.text.strip()

        fest_place_parant = fest_date_info.find_parent().find_parent().find_next_sibling()
        fest_place = fest_place_parant.find("span").text.strip()


        print(count)
        print(fest_name)
        print(fest_date)
        print(fest_place)
        print(url)
        print("-" * 20)

        #ПОЛУЧАЕМ КОНТАКТЫ И ИНФОРМАЦИЮ (НАВЕРНОЕ)
        fest_list_result.append(
            {
                "Fest name": fest_name,
                "Fest date": fest_date,
                "Fest location": fest_place
            }
        )
    except Exception as ex:
        print(ex)
        print("Error")

with open("fest_list_result.json", "a", encoding="utf-8") as file:
    json.dump(fest_list_result, file, indent=4, ensure_ascii=False)