import json

def json_read():
    """
    Читает данные из файла pupirky.json.
    Возвращает список словарей или пустой список, если файл не существует или поврежден.
    """
    try:
        with open("data/pupirky.json", 'r') as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Файл data/pupirky.json не найден. Создаю новый файл.")
        return []  # Возвращаем пустой список, если файл не существует
    except json.JSONDecodeError:
        print("Файл data/pupirky.json содержит некорректные данные.")
        return []

def json_write(pup_name, pup_count, pup_type):
    """
    Добавляет новую запись в JSON-файл.
    Если запись с таким именем уже существует, ничего не делает.
    """
    data = json_read()
    flag = False
    # Проверяем, есть ли уже запись с таким именем
    for i in range(len(data)):
        if data[i]["pup_name"] == pup_name:
            print(f"Changed {pup_name}")
            data[i]["pup_count"] += pup_count
            flag = True
            break


    # Добавляем новую запись
    if not flag:
        data.append({"pup_name": pup_name, "pup_count": pup_count, "pup_type": pup_type})

    # Записываем обновленные данные в файл
    with open("data/pupirky.json", 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Added {pup_name} {pup_count} {pup_type}")

def watch_pup():
    """
    Выводит текущее состояние данных в консоль.
    """
    pups = json_read()
    
    print("########\n# PUPS #\n########")
    
    for i, pup in enumerate(pups):
        a = pup["pup_name"]
        b = pup["pup_count"]

        c = pup["pup_type"]
        if c == "0":
            c = "weed"
        elif c == "1":
            c = "meth"
        elif c == "2":
            c = "geroine"
        else:
            c = "unknown"

        print(f"{i + 1} - {a} {b} {c}")
    
    print("########")

def remove_pup(name):
    """
    Удаляет запись по имени.
    Возвращает удаленную запись или пустой словарь, если запись не найдена.
    """
    data = json_read()

    # Ищем запись по имени
    for pup in data:
        if pup["pup_name"] == name:
            data.remove(pup)  # Удаляем запись

            # Перезаписываем файл
            with open("data/pupirky.json", 'w') as file:
                json.dump(data, file, indent=4)

            print(f"Deleted: {pup['pup_name']} {pup['pup_count']} {pup['pup_type']}")
            return pup  # Возвращаем удаленную запись

    print("Not found! Nothing to do.")
    return {"pup_name": "", "pup_count": "", "pup_type": ""}

def catch_pup(name, count_to_catch):
    """
    "Захватывает" указанное количество предметов.
    Возвращает True, если захват выполнен успешно, иначе False.
    """
    data = json_read()

    for pup in data:
        if pup["pup_name"] == name:
            if pup["pup_count"] >= count_to_catch:
                pup["pup_count"] -= count_to_catch  # Уменьшаем количество

                # Если количество стало равным нулю, удаляем запись
                if pup["pup_count"] == 0:
                    data.remove(pup)
                    print(f"Deleted {name} (count reached 0)")

                # Перезаписываем файл
                with open("data/pupirky.json", 'w') as file:
                    json.dump(data, file, indent=4)

                print(f"Catched {count_to_catch} of {pup['pup_name']} (remaining: {pup['pup_count']})")
                return True
            else:
                print(f"Not enough items to catch! Available: {pup['pup_count']}")
                return False

    print("Item not found!")
    return False

def search_pup(name):
    """
    Ищет запись по имени.
    Возвращает найденную запись или пустой словарь, если запись не найдена.
    """
    data = json_read()

    for pup in data:
        if pup["pup_name"] == name:
            print(f"Found: {pup['pup_name']} {pup['pup_count']} {pup['pup_type']}")
            return pup

    print("Not found!")
    return {"pup_name": "", "pup_count": "", "pup_type": ""}

def get_pups_as_text():
    """
    Возвращает текущее состояние данных в виде текста для отправки в бот.
    """
    pups = json_read()
    
    if not pups:
        return "No items available."

    result = "########\n# PUPS #\n########\n"
    
    for i, pup in enumerate(pups):
        a = pup["pup_name"]
        b = pup["pup_count"]

        c = pup["pup_type"]
        if c == "0":
            c = "weed"
        elif c == "1":
            c = "meth"
        elif c == "2":
            c = "geroine"
        else:
            c = "unknown"

        result += f"{i + 1}. {a} - {b} ({c})\n"
    
    result += "########"
    return result