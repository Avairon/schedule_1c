import json
import os

def json_read():
    with open("data/pupirky.json", 'r') as file: # read the json
        data = json.load(file)
        
    return data


def json_write(pup_name, pup_count, pup_type):
    data = json_read()

    data.append({"pup_name": pup_name, "pup_count": pup_count, "pup_type": pup_type})

    file = open('data/pupirky.json', 'w')

    content = json.dumps(data)
    file.write(content)
    file.close()

def print_menu() -> int:
    choice = -2

    print("============\n1 - Insert pupiryshki\n2 - Remove pupiryshki\n3 - Catch from pupiryshki\n4 - Search pupiryshki\nq - exit\n============")
    
    choice = str(input("Choice: "))
    return choice

def watch_pup():
    pups = json_read()
    
    print("########\n# PUPS #\n########")
    
    for i in range(len(pups)):
        a = pups[i]["pup_name"]
        b = pups[i]["pup_count"]

        c = pups[i]["pup_type"]
        
        if(c == "0"):
            c = "weed"
        elif(c == "1"):
            c = "meth"
        elif(c == "2"):
            c = "geroine"
        else:
            c = "unknown"

        print(f"{i + 1} - {a} {b} {c}")
    
    print("########")

def write_pup() -> None:
    try:
        name = input("------------\ninsert pup name: ")

        data = json_read()

        for i in data:
            if(name == i["pup_name"]):
                print("Already exist! Nothing be do.\n------------")
                return

        try:
            count = int(input("insert pup count: "))
        except Exception as e:
            print("Uncorrect input! Try again")
            return

        type_ = input("insert pup type(0 - weed, 1 - meth, 2 - geroine): ")

        json_write(name, count, type_)

        print(f"------------\nAdded {name} {count} {type_}\n------------")
    except Exception as e:
        print("Error!")

def remove_pup() -> list:
    name = str(input("------------\nInsert name: "))
    data = json_read()
    
    count = 0
    
    for i in data:
        if(name == i["pup_name"]):
            count = 1
            out = i
            break

        if(name == i["pup_name"][:len(name)]):
            count += 1
            out = i

    if(count != 1):
        print("Not found! Nothing be do.\n------------")
        return {"pup_name": "", "pup_count": "", "pup_type": ""}
    else:
        a = out["pup_name"]
        b = out["pup_count"]

        print(f"------------\nSelected {a} {b}")

    a = out["pup_name"]
    b = out["pup_count"]
    c = out["pup_type"]

    print(f"------------\nYou want delete {a} {b} {c}")
    choice = str(input("Are you sure? (y/n): "))

    if(choice[0] != "y" and choice[0] != "Y"):
        return out

    updated_data = []

    for pup in data:
        if pup == out:
            continue
        updated_data.append(pup)  # Добавляем остальные записи

    with open("data/pupirky.json", 'w') as file:
        json.dump(updated_data, file, indent=4)
 
    print(f"------------\nDeleted: {a} {b} {c}\n------------")

    return out

def catch_pup() -> None:
    name = str(input("------------\nInsert name: "))

    count_f = 0
    data = json_read()

    for i in data:
        if(name == i["pup_name"]):
            count_f = 1
            out = i
            break

        if(name == i["pup_name"][:len(name)]):
            count_f += 1
            out = i

    if(count_f != 1):
        print("Not found! Nothing be do.\n------------")
        return {"pup_name": "", "pup_count": "", "pup_type": ""}
    else:
        a = out["pup_name"]
        b = out["pup_count"]

        print(f"------------\nSelected {a} {b}")

    count = str(input("Insert count: "))

    catched = 0
    ends = False

    for i in range(len(data)):
        if(data[i] == out):
            if(data[i]["pup_count"] >= int(count)):
                catched = count
                data[i]["pup_count"] -= int(count)
                name = data[i]["pup_name"]

                if(data[i]["pup_count"] == 0):
                    print(f"------------\nCatched, ends {name} {count}\n------------")
                    ends = True

                print(f"------------\nCatched {name} {count}\n------------")
                break
            else:
                catched = data[i]["pup_count"]
                data[i]["pup_count"] -= int(count)
                name = data[i]["pup_name"]
                print(f"------------\nNot enought. Catched {name} {catched}\n------------")
                ends = True
                break

    updated_data = data

    if(ends):
        updated_data = []
        for pup in data:
            if pup == out:
                continue
            updated_data.append(pup)  # Добавляем остальные записи

    with open("data/pupirky.json", 'w') as file:
        json.dump(updated_data, file, indent=4)

    return

def search_pup() -> None:
    name = str(input("------------\nInsert name: "))

    count_f = 0
    data = json_read()

    for i in data:
        if(name == i["pup_name"]):
            count_f = 1
            out = i
            break

        if(name == i["pup_name"][:len(name)]):
            count_f += 1
            out = i

    if(count_f != 1):
        print("Not found! Nothing be do.\n------------")
        
    else:
        a = out["pup_name"]
        b = out["pup_count"]
        c = out["pup_type"]

        print(f"------------\nSearched: {a} {b} {c}\n------------")
    
    return

if __name__ == "__main__":
    watch_pup()
    choice = str(print_menu())
    os.system('cls')

    while choice[0] != "q":
        if(choice[0] == "1"):
            write_pup()
        
        if(choice[0] == "2"):
            remove_pup()

        if(choice[0] == "3"):
            catch_pup()
        
        if(choice[0] == "4"):
            search_pup()
        
        watch_pup()
        choice = str(print_menu())
        os.system('cls')
         


