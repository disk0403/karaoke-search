import sqlite3

con = sqlite3.connect('karaoke_search.db')
c = con.cursor()

pref_rows = list(c.execute('SELECT pref_code, pref FROM pref'))
city_rows = list(c.execute('SELECT city_code, pref_code, city FROM city'))
condition_rows = list(c.execute('SELECT condition_code, condition FROM condition'))

for pref_row in pref_rows:
    print(f"{int(pref_row[0]):>2}. {pref_row[1]}")

message = "数字を入力して都道府県を選択してください: "

while True:
    selected_pref_code = input(message).translate(str.maketrans("０１２３４５６７８９", "0123456789"))

    if selected_pref_code.isdigit() and 1 <= int(selected_pref_code) <= 47:
        break

    message = "1-47の整数値で入力してください: "

selected_city_rows = []

for city_row in city_rows:
    if city_row[1] == int(selected_pref_code):
        selected_city_rows.append(city_row)

city_number = len(selected_city_rows)

print()
for index, city_row in enumerate(selected_city_rows, start=1):
    print(f"{index:>3}. {city_row[2]}")

message = "数字を入力して市区町村を選択してください: "

while True:
    selected_city_number = input(message).translate(str.maketrans("０１２３４５６７８９", "0123456789"))

    if selected_city_number.isdigit() and 1 <= int(selected_city_number) <= city_number:
        break

    message = f"1-{city_number}の整数値で入力してください: "

selected_city_row = selected_city_rows[int(selected_city_number) - 1]
selected_city_code = selected_city_row[0]

print()
print("0. 条件なし")

for condition_row in condition_rows:
    print(f"{condition_row[0]}. {condition_row[1]}")

valid_condition_codes = {str(condition_row[0]) for condition_row in condition_rows}
message = "0、または条件番号の組み合わせを入力してください: "

while True:
    selected_condition_numbers = input(message).translate(str.maketrans("０１２３４５６７８９", "0123456789"))

    if selected_condition_numbers == "0" or set(selected_condition_numbers) <= valid_condition_codes:
        break

    message = "0、または条件番号の組み合わせで入力してください: "

if selected_condition_numbers == "0":
    selected_conditions = set()
else:
    selected_conditions = {int(number) for number in selected_condition_numbers}

print()
print("検索結果")
print("-------------------------------------------")
result_count = 0

if not selected_conditions:
    sql = 'SELECT branch, address, url_branch FROM branch_info WHERE city_code = ?'
    data = (selected_city_code,)
    result = c.execute(sql, data)

else:
    sql = '''
        SELECT branch_info.branch, branch_info.address, branch_info.url_branch
        FROM branch_info
        INNER JOIN branch_condition
        ON branch_info.branch_code = branch_condition.branch_code
        WHERE branch_info.city_code = ?
        AND branch_condition.condition_code IN ({})
        GROUP BY branch_info.branch_code
        HAVING COUNT(DISTINCT branch_condition.condition_code) = ?
    '''.format(",".join("?" * len(selected_conditions)))

    data = (selected_city_code,) + tuple(selected_conditions) + (len(selected_conditions),)
    result = c.execute(sql, data)

for row in result:
    result_count += 1
    print(row[0])
    print(row[1])
    print(row[2])
    print("-------------------------------------------")

if result_count == 0:
    print("該当する店舗はありません。")

con.close()
