import requests

SERVER_URL = "http://<server-ip>:5000"  # Замените <server-ip> на IP-адрес сервера

# Получение всех записей
def watch_pups():
    response = requests.get(f"{SERVER_URL}/pups")
    if response.status_code == 200:
        pups = response.json()
        print("########\n# PUPS #\n########")
        for i, pup in enumerate(pups):
            pup_type = {
                "0": "weed",
                "1": "meth",
                "2": "geroine"
            }.get(pup["pup_type"], "unknown")
            print(f"{i + 1} - {pup['pup_name']} {pup['pup_count']} {pup_type}")
        print("########")
    else:
        print(f"Error: {response.status_code}")

# Добавление новой записи
def write_pup():
    name = input("Insert pup name: ")
    try:
        count = int(input("Insert pup count: "))
    except ValueError:
        print("Uncorrect input! Try again")
        return
    type_ = input("Insert pup type (0 - weed, 1 - meth, 2 - geroine): ")

    new_pup = {"pup_name": name, "pup_count": count, "pup_type": type_}
    response = requests.post(f"{SERVER_URL}/pups", json=new_pup)

    if response.status_code in (200, 201):
        print(response.json()["message"])
    else:
        print(f"Error: {response.status_code}")

# Удаление записи
def remove_pup():
    name = input("Insert name to delete: ")
    response = requests.delete(f"{SERVER_URL}/pups/{name}")

    if response.status_code == 200:
        print(response.json()["message"])
    elif response.status_code == 404:
        print(response.json()["error"])
    else:
        print(f"Error: {response.status_code}")

# Поиск записи
def search_pup():
    name = input("Insert name to search: ")
    response = requests.get(f"{SERVER_URL}/pups/search/{name}")

    if response.status_code == 200:
        results = response.json()
        print("Search results:")
        for pup in results:
            pup_type = {
                "0": "weed",
                "1": "meth",
                "2": "geroine"
            }.get(pup["pup_type"], "unknown")
            print(f"{pup['pup_name']} {pup['pup_count']} {pup_type}")
    elif response.status_code == 404:
        print(response.json()["error"])
    else:
        print(f"Error: {response.status_code}")

# Главное меню
def print_menu():
    print("============\n1 - Insert pupiryshki\n2 - Remove pupiryshki\n3 - Search pupiryshki\nq - exit\n============")
    return input("Choice: ")

if __name__ == "__main__":
    choice = print_menu()

    while choice[0] != "q":
        if choice[0] == "1":
            write_pup()
        elif choice[0] == "2":
            remove_pup()
        elif choice[0] == "3":
            search_pup()
        elif choice[0] == "q":
            break
        else:
            print("Invalid choice!")

        watch_pups()
        choice = print_menu()