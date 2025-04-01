from project.parser import save_to_file, parser_restaurants

if __name__ == "__main__":
    print("🚀 Запуск парсинга ...")
    restaurants = parser_restaurants()
    print("\n💾 Сохранение ...")
    save_to_file(restaurants)
