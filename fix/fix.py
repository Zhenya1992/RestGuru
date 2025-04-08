import re


input_file = 'restaurants_Mozyr.md'
fixed_file = 'fixed_links.md'

def fix(input_file, fixed_file):
    with open(input_file, 'r', encoding='UTF-8') as f:
        data = f.read()

    fixed_data = re.sub(
        r"https://ru\.restaurantguru\.com/([^\s\)\]]+)",
        r"https://restaurantguru.ru/\1",
        data
    )

    with open(fixed_file, 'w', encoding="UTF-8") as f:
        f.write(fixed_data)

    print("Ссылки успешно исправлены")


fix(input_file, fixed_file)