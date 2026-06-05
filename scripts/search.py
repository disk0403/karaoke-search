import csv
from dict_pref_city import dict_pref, dict_city, dict_pref_city_id

for pref_id, pref in dict_pref.items():
    print(f"{int(pref_id):>2}. {pref['name']}")

message = "数字を入力して都道府県を選択してください: "

while True:
    selected_pref_id = input(message).translate(str.maketrans("０１２３４５６７８９", "0123456789"))

    if selected_pref_id.isdigit() and 1 <= int(selected_pref_id) <= 47:
        selected_pref_id = selected_pref_id.zfill(2)
        break

    message = "1-47の整数値で入力してください: "

city_ids = dict_pref_city_id[selected_pref_id]
city_number = len(city_ids)

print()
for unique_id in city_ids:
    city = dict_city[unique_id]
    print(f"{int(city['city_id']):>3}. {city['name']}")

message = "数字を入力して市区町村を選択してください: "

while True:
    selected_city_id = input(message).translate(str.maketrans("０１２３４５６７８９", "0123456789"))

    if selected_city_id.isdigit() and 1 <= int(selected_city_id) <= city_number:
        selected_city_id = selected_city_id.zfill(3)
        break

    message = f"1-{city_number}の整数値で入力してください: "

selected_unique_id = selected_pref_id + selected_city_id
selected_pref = dict_pref[selected_pref_id]["name"]
selected_city = dict_city[selected_unique_id]["name"]

print()
print("0. 条件なし")
print("1. 駐車場有")
print("2. Wi-Fi有")
print("3. 持ち込み可")
print("4. 喫煙所有")
message = "0、または1-4の数字の組み合わせを入力して条件を選択してください: "

while True:
    selected_condition_numbers = input(message).translate(str.maketrans("０１２３４５６７８９", "0123456789"))

    if selected_condition_numbers == "0" or set(selected_condition_numbers) <= set("1234"):
        break

    message = "0、または1-4の組み合わせで入力してください: "

if selected_condition_numbers == "0":
    selected_conditions = []
else:
    selected_conditions = list(selected_condition_numbers)

condition = {
    "1": "parking",
    "2": "wifi",
    "3": "bringin",
    "4": "smoking",
}

print()
print("検索結果")
print("-------------------------------------------")
result_count = 0

with open("local/branches.csv", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)

    for branch in reader:
        if branch["pref"] != selected_pref:
            continue

        if branch["city"] != selected_city:
            continue

        match = True

        for condition_number in selected_conditions:
            column = condition[condition_number]

            if branch[column] != "1":
                match = False
                break

        if match:
            result_count += 1
            print(branch["branch"])
            print(branch["address"])
            print(branch["url"])
            print("-------------------------------------------")

if result_count == 0:
    print("該当する店舗はありません。")
