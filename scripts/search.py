import csv

def read_csv(path):
    with open(path, encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))

pref_rows = read_csv("db/pref.csv")
city_rows = read_csv("db/city.csv")
condition_rows = read_csv("db/condition.csv")
branch_info_rows = read_csv("local/branch_info.csv")
branch_condition_rows = read_csv("local/branch_condition.csv")

for pref_row in pref_rows:
    print(f"{int(pref_row['pref_code']):>2}. {pref_row['pref']}")

message = "数字を入力して都道府県を選択してください: "

while True:
    selected_pref_code = input(message).translate(str.maketrans("０１２３４５６７８９", "0123456789"))

    if selected_pref_code.isdigit() and 1 <= int(selected_pref_code) <= 47:
        break

    message = "1-47の整数値で入力してください: "

selected_city_rows = []

for city_row in city_rows:
    if city_row["pref_code"] == selected_pref_code:
        selected_city_rows.append(city_row)

city_number = len(selected_city_rows)

print()
for index, city_row in enumerate(selected_city_rows, start=1):
    print(f"{index:>3}. {city_row['city']}")

message = "数字を入力して市区町村を選択してください: "

while True:
    selected_city_number = input(message).translate(str.maketrans("０１２３４５６７８９", "0123456789"))

    if selected_city_number.isdigit() and 1 <= int(selected_city_number) <= city_number:
        break

    message = f"1-{city_number}の整数値で入力してください: "

selected_city_row = selected_city_rows[int(selected_city_number) - 1]
selected_city_code = selected_city_row["city_code"]

print()
print("0. 条件なし")

for condition_row in condition_rows:
    print(f"{condition_row['condition_code']}. {condition_row['condition']}")

valid_condition_codes = {condition_row["condition_code"] for condition_row in condition_rows}
message = "0、または条件番号の組み合わせを入力してください: "

while True:
    selected_condition_numbers = input(message).translate(str.maketrans("０１２３４５６７８９", "0123456789"))

    if selected_condition_numbers == "0" or set(selected_condition_numbers) <= valid_condition_codes:
        break

    message = "0、または条件番号の組み合わせで入力してください: "

if selected_condition_numbers == "0":
    selected_conditions = set()
else:
    selected_conditions = set(selected_condition_numbers)

branch_conditions = {}

for row in branch_condition_rows:
    branch_code = row["branch_code"]
    condition_code = row["condition_code"]

    if branch_code not in branch_conditions:
        branch_conditions[branch_code] = set()

    branch_conditions[branch_code].add(condition_code)

print()
print("検索結果")
print("-------------------------------------------")
result_count = 0

for branch in branch_info_rows:
    if branch["city_code"] != selected_city_code:
        continue

    available_conditions = branch_conditions.get(branch["branch_code"], set())

    if not selected_conditions <= available_conditions:
        continue

    result_count += 1
    print(branch["branch"])
    print(branch["address"])
    print(branch["url_branch"])
    print("-------------------------------------------")

if result_count == 0:
    print("該当する店舗はありません。")
