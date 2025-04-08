import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re


async def main_parser(md_file_path, output_file_path):
    """ """

    restaurant_links = read_restaurant_links_from_md(md_file_path)

    restaurant_info = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            headless=True
        )

        for index, link in enumerate(restaurant_links[:22], start=1):
            try:
                print(f" Ищу на странице: {link}")

                context = await browser.new_context(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                    extra_http_headers={
                        "Accept-Language": "en-US,en;q=0.9"
                    }
                )
                page = await context.new_page()

                if await load_page_with_retry(page, link):
                    await page.wait_for_selector('a[href^="tel:"]', timeout=50000)

                    html = await page.content()
                    soup = BeautifulSoup(html, "html.parser")

                    name_tag = soup.find("a", {"style": "opacity: 1;"})
                    name = name_tag.get_text(strip=True) if name_tag else "Неизвестно"

                    phone_tag = soup.find("a", href=re.compile(r"tel:\+?\d+"))
                    phone_number = phone_tag.get_text(strip=True) if phone_tag else "Не найден"

                    print(f"📞 Найден номер: {phone_number}, Название: {name}")
                    restaurant_info.append(f"{index}. {name} : {phone_number}")
                    await page.close()

                else:
                    print(f"😩 Не удалось загрузить страницу {link} после нескольких попыток.")
            except Exception as e:
                print(f" Ошибка при обработке {link}: {e}")

        await browser.close()

    save_restaurant_info_to_md(output_file_path, restaurant_info)


def save_restaurant_info_to_md(output_file_path, restaurant_info):
    """Сохраняет найденную информацию о ресторанах в markdown файл."""

    with open(output_file_path, "w", encoding="utf-8") as file:
        file.write("# Информация о ресторанах\n\n")
        for line in restaurant_info:
             file.write(f"{line}\n")


async def load_page_with_retry(page, url, retries=2):
    """Доп попытки загрузки"""

    for attempt in range(retries):
        try:
            print(f"Попытка {attempt + 1} для {url}")
            await page.goto(url, timeout=60000)
            await page.wait_for_selector('a[href^="tel:"]', timeout=40000)
            return True
        except Exception as e:
            print(f"Попытка {attempt + 1} не удалась для {url}: {e}")
            await asyncio.sleep(3)
    return False



def read_restaurant_links_from_md(md_file_path):

    links = []
    with open(md_file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = re.search(r"\[(?:Ссылка|.*?)\]\((https://restaurantguru\.ru/.*?)\)", line)
            if match:
                links.append(match.group(1))
    return links


