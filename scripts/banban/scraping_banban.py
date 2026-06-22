import bs4
import requests
import sqlite3

def get_address(info_branch, pref):
    text = info_branch.find("div", id="sss").get_text(" ", strip=True)
    start = text.find(pref)
    end = text.find("TEL:")
    address = text[start:end].strip()
    return address

def get_city_code(address, pref):
    pref_code = ""

    for pref_row in pref_rows:
        if pref_row[1] == pref:
            pref_code = pref_row[0]
            break

    for city_row in city_rows:
        if city_row[1] != pref_code:
            continue

        if city_row[2] in address:
            return city_row[0]

    return ""

con = sqlite3.connect('karaoke_search.db')
c = con.cursor()

c.executescript('''
    CREATE TABLE branch_info(
        branch_code INTEGER primary key,
        chain_code INTEGER,
        city_code INTEGER,
        branch TEXT,
        address TEXT,
        url_branch TEXT
    );

    CREATE TABLE branch_condition(
        branch_code INTEGER,
        condition_code INTEGER,
        PRIMARY KEY(branch_code, condition_code)
    );
''')

pref_rows = list(c.execute("SELECT pref_code, pref FROM pref"))
city_rows = list(c.execute("SELECT city_code, pref_code, city FROM city"))
condition_code_by_alt = {"専用・共有駐車場": 1, "提携駐車場": 1, "Wi-Fi": 2, "持ち込みOK": 3, "喫煙所": 4}
chain_code = 1
branch_code = 0

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

        sql = 'INSERT INTO branch_info(branch_code, chain_code, city_code, branch, address, url_branch) VALUES(?, ?, ?, ?, ?, ?)'
        data = (branch_code, chain_code, city_code, branch, address, url_branch)
        c.execute(sql, data)

        sql = 'INSERT INTO branch_condition(branch_code, condition_code) VALUES(?, ?)'
        for condition_code in sorted(set(condition_codes)):
            data = (branch_code, condition_code)
            c.execute(sql, data)

con.commit()
con.close()
