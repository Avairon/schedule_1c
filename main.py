import json

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

    print("============\n0 - Watch pypiryshki\n1 - Insert pupiryshki\n2 - Remove pupiryshki\n3 - Catch from pupiryshki\n4 - Search pupiryshki\nq - exit\n============")
    
    choice = str(input("Choice: "))
    return choice

def watch_pup():
    pups = json_read()
    
    print("########\n# PUPS #\n########")
    
    for i in range(len(pups)):
        print(f"{i + 1} - {pups[i]["pup_name"]} {pups[i]["pup_count"]} {pups[i]["pup_type"]}")
    
    print("########")

def write_pup() -> None:
    try:
        name = input("insert pup name: ")
        try:
            count = int(input("insert pup count: "))
        except Exception as e:
            print("Uncorrect input! Try again")
            return

        type_ = input("insert pup type: ")

        json_write(name, count, type_)

        print(f"Added {name} {count} {type_}")
    except Exeption as e:
        print("Error!")

def remove_pup() -> str:
    name = str(input("Insert name: "))
    data = json_read()
    
    out = ""
    count = 0
    
    for i in data:
        if(name == i["pup_name"]):
            count = 1
            out = i["pup_name"]
            break

        if(name == i["pup_name"][:len(name)]):
            count += 1
            out = i["pup_name"]

    if(count == 1):
        return f"good {count} {out}"
    else:
        return f"bad {count}"

if __name__ == "__main__":
    choice = str(print_menu())

    while choice[0] != "q":
        if(choice[0] == "0"):
            watch_pup()

        if(choice[0] == "1"):
            write_pup()
        
        if(choice[0] == "2"):
            print(remove_pup())

        choice = str(print_menu())
         


