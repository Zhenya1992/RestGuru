import asyncio
from pathlib import Path
from project.parser import parser_restaurants, save_to_file
from project.main_parser import main_parser


BASE_DIR = Path("D:\Python\Projects\RestGuru")
PRE_DATA_DIR = BASE_DIR / "pre_data"
OUTPUT_DIR = BASE_DIR / "output_files"

MD_FILE_PATH = PRE_DATA_DIR / "fixed_links.md"
OUTPUT_FILE_PATH = OUTPUT_DIR / "data_Zlobin.md"

async def run():
    print("🚀 Запуск парсинга ресторанов...")
    restaurants = parser_restaurants()

    if not restaurants:
        print("Ошибка: Не удалось получить список ресторанов!")
        return


    PRE_DATA_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("\n💾 Сохранение данных...")
    save_to_file(restaurants, PRE_DATA_DIR)

    print("\n Запуск парсинга номеров телефонов...")
    await main_parser(MD_FILE_PATH, OUTPUT_FILE_PATH)
    print("✅ Парсинг завершен ")

if __name__ == "__main__":
    asyncio.run(run())