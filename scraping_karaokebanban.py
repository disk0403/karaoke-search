import csv
import bs4
import requests
from dict_pref_city import dict_pref, dict_city

rows = []

url = "https://karaoke-shin.jp/shop-list/#freeResearch"
r = requests.get(url)
s = bs4.BeautifulSoup(r.text, "html.parser")

def get_address(info_branch, pref):
    text = info_branch.find("div", id="sss").get_text(" ", strip=True)
    start = text.find(pref)
    end = text.find("TEL:")
    address = text[start:end].strip()
    return address

def get_city(address, pref):
    city = ""
    pref_id = ""

    for pref_data in dict_pref.values():
        if pref in pref_data["alias"]:
            pref_id = pref_data["pref_id"]
            break

    for city_data in dict_city.values():
        if city_data["pref_id"] != pref_id:
            continue

        for city_alias in city_data["alias"]:
            if city_alias in address:
                city = city_data["name"]
                return city

    return city

for link_pref in s.find_all("area", shape = "rect"):
    url_pref = link_pref["href"]
    r_pref = requests.get(url_pref)
    s_pref = bs4.BeautifulSoup(r_pref.text, "html.parser")
    pref = s_pref.find("div", class_ = "breadlist").find_all("li")[2].string

    for info_branch in s_pref.find_all("li", class_ = "clearfix"):
        branch = info_branch.a.string
        url_branch = info_branch.a["href"]
        address = get_address(info_branch, pref)
        city = get_city(address, pref)
        parking, wifi, bringin, smoking = 0, 0, 0, 0

        for img_tag in info_branch.find_all("img"):
            alt = img_tag.get("alt")
            if alt == "専用・共有駐車場":
                parking = 1
            elif alt == "提携駐車場":
                parking = 1
            elif alt == "Wi-Fi":
                wifi = 1
            elif alt == "持ち込みOK":
                bringin = 1
            elif alt == "喫煙所":
                smoking = 1

        rows.append(["カラオケBanBan", branch, url_branch, pref, city, address, parking, wifi, bringin, smoking])

with open("branches.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["chain", "branch", "url", "pref", "city", "address", "parking", "wifi", "bringin", "smoking"])
    writer.writerows(rows)