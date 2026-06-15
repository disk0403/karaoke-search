import csv
import bs4
import requests

branch_info_rows = []
branch_condition_rows = []
pref_rows = []
city_rows = []
chain_code = 1
branch_code = 0
condition_code_by_alt = {"専用・共有駐車場": 1, "提携駐車場": 1, "Wi-Fi": 2, "持ち込みOK": 3, "喫煙所": 4,}

with open("db/pref.csv", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    pref_rows = list(reader)

with open("db/city.csv", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)
    city_rows = list(reader)

def get_address(info_branch, pref):
    text = info_branch.find("div", id="sss").get_text(" ", strip=True)
    start = text.find(pref)
    end = text.find("TEL:")
    address = text[start:end].strip()
    return address

def get_city_code(address, pref):
    pref_code = ""

    for pref_row in pref_rows:
        if pref_row["pref"] == pref:
            pref_code = pref_row["pref_code"]
            break

    for city_row in city_rows:
        if city_row["pref_code"] != pref_code:
            continue

        if city_row["city"] in address:
            return city_row["city_code"]

    return ""

url = "https://karaoke-shin.jp/shop-list/#freeResearch"
r = requests.get(url)
s = bs4.BeautifulSoup(r.text, "html.parser")

for link_pref in s.find_all("area", shape = "rect"):
    url_pref = link_pref["href"]
    r_pref = requests.get(url_pref)
    s_pref = bs4.BeautifulSoup(r_pref.text, "html.parser")
    pref = s_pref.find("div", class_ = "breadlist").find_all("li")[2].string

    for info_branch in s_pref.find_all("li", class_ = "clearfix"):
        branch_code += 1
        branch = info_branch.a.string
        url_branch = info_branch.a["href"]
        address = get_address(info_branch, pref)
        city_code = get_city_code(address, pref)
        condition_codes = []

        for img_tag in info_branch.find_all("img"):
            alt = img_tag.get("alt")
            condition_code = condition_code_by_alt.get(alt)

            if condition_code:
                condition_codes.append(condition_code)

        for condition_code in sorted(set(condition_codes)):
            branch_condition_rows.append([branch_code, condition_code])

        branch_info_rows.append([branch_code, chain_code, city_code, branch, address, url_branch])
        
with open("local/branch_info.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["branch_code", "chain_code", "city_code", "branch", "address", "url_branch"])
    writer.writerows(branch_info_rows)

with open("local/branch_condition.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["branch_code", "condition_code"])
    writer.writerows(branch_condition_rows)
