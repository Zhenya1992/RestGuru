from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from pathlib import Path


# Настройка Selenium
def setup_driver():
    """Настройки и запуск драйвера"""

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("start-maximized")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    return driver


def parser_restaurants():
    """Парсинг списков ресторанов(id, название и ссылка) и возвращает данные в виде списка словарей"""

    driver = setup_driver()
    url = 'https://restaurantguru.ru/Mazyr'
    driver.get(url)
    time.sleep(3)

    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

    restaurants = []
    restaurant_cards = driver.find_elements(By.CLASS_NAME, "rest_info")
    if not restaurant_cards:
        print("Ошибка: информация не найдена")
        driver.quit()
        return []

    for card in restaurant_cards:
        try:
            name = card.find_element(By.CLASS_NAME, "title").text.strip()
            link = card.find_element(By.CLASS_NAME, "title").get_attribute("href")
            restaurant_id = link.split("/")[-1] if link else "N/A"

            restaurants.append({
                "Название": name,
                "ID": restaurant_id,
                "Ссылка": link
            })
        except Exception as e:
            print(f"Ошибка при парсинге ресторана: {e}")
            continue

    driver.quit()
    return restaurants


def save_to_file(data, output_dir=None, output_file='restaurants_Mozyr.md'):
    if not data:
        print("Ошибка: нет данных")
        return
    if output_dir is None:
        output_dir = Path.cwd() / "pre_data"

    output_path = Path(output_dir) / output_file
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open('w', encoding='utf-8') as file:
        file.write("# 📌 Список ресторанов \n\n")
        file.write("| №  | Название | ID | Ссылка |\n")
        file.write("|----|----------|----|--------|\n")

        for idx, row in enumerate(data, start=1):
            name = row.get("Название", "").strip() or "Неизвестно"
            restaurant_id = row.get("ID", "").strip() or "N/A"
            link = row.get("Ссылка", "").strip()

            name_link = f"[{name}]({link})" if link else name
            link_md = f"[Ссылка]({link})" if link else "Нет ссылки"

            file.write(f"| {idx} | {name_link} | {restaurant_id} | {link_md} |\n")

    print(f"✅ Данные успешно сохранены в {output_path}")

res = parser_restaurants()
save_to_file(res)