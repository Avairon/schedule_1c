from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
DATABASE_FILE = "data/pupirky.json"

# Проверка существования файла базы данных
if not os.path.exists(DATABASE_FILE):
    os.makedirs(os.path.dirname(DATABASE_FILE), exist_ok=True)
    with open(DATABASE_FILE, "w") as f:
        json.dump([], f)

# Вспомогательная функция для чтения данных из JSON
def json_read():
    with open(DATABASE_FILE, 'r') as file:
        data = json.load(file)
    return data

# Вспомогательная функция для записи данных в JSON
def json_write(data):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)

# Получение всех записей
@app.route('/pups', methods=['GET'])
def get_pups():
    data = json_read()
    return jsonify(data)

# Добавление новой записи
@app.route('/pups', methods=['POST'])
def add_pup():
    new_pup = request.json
    data = json_read()

    # Проверяем, существует ли запись с таким же именем
    for pup in data:
        if pup["pup_name"] == new_pup["pup_name"]:
            pup["pup_count"] += new_pup["pup_count"]
            json_write(data)
            return jsonify({"message": f"Updated {new_pup['pup_name']} count"}), 200

    # Если запись не найдена, добавляем новую
    data.append(new_pup)
    json_write(data)
    return jsonify({"message": f"Added {new_pup['pup_name']}"}), 201

# Удаление записи
@app.route('/pups/<string:name>', methods=['DELETE'])
def delete_pup(name):
    data = json_read()
    updated_data = [pup for pup in data if pup["pup_name"] != name]

    if len(updated_data) == len(data):
        return jsonify({"error": f"Pupiryshka '{name}' not found"}), 404

    json_write(updated_data)
    return jsonify({"message": f"Deleted {name}"}), 200

# Поиск записи по имени
@app.route('/pups/search/<string:name>', methods=['GET'])
def search_pup(name):
    data = json_read()
    result = [pup for pup in data if name.lower() in pup["pup_name"].lower()]
    if not result:
        return jsonify({"error": f"Pupiryshka '{name}' not found"}), 404
    return jsonify(result), 200

@app.route('/pups/add/<string:name>/<int:count>', methods=['POST'])
def add_pupp(name, count):
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
        #print("Not found! Nothing be do.\n------------")
        return jsonify({"error": f"Pupiryshka '{name}' not found"}), 404

        #print(f"------------\nSelected {a}, count: {b}")

    out_res = jsonify({"error": f"Pupiryshka '{name}' not found"}), 404

    for i in range(len(data)):
        if(data[i] == out):
            data[i]["pup_count"] += int(count)
            out_res = jsonify({
                "message": f"Added {count} to {data[i]['pup_name']}. Remaining: {data[i]['pup_count']}"
            }), 200

    with open("data/pupirky.json", 'w') as file:
        json.dump(data, file, indent=4)

    # Если запись не найдена
    return out_res

@app.route('/pups/catch/<string:name>/<int:count>', methods=['POST'])
def catch_pup(name, count):
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
        #print("Not found! Nothing be do.\n------------")
        return jsonify({"error": f"Pupiryshka '{name}' not found"}), 404

        #print(f"------------\nSelected {a}, count: {b}")

    out_res = jsonify({"error": f"Pupiryshka '{name}' not found"}), 404

    ends = False

    for i in range(len(data)):
        if(data[i] == out):
            if(data[i]["pup_count"] >= int(count)):
                data[i]["pup_count"] -= int(count)
                name = data[i]["pup_name"]

                if(data[i]["pup_count"] == 0):
                    ends = True
                    out_res = jsonify({
                        "message": f"Catched {count} from {name}. Ends."
                    }), 200
                else:
                    out_res = jsonify({
                        "message": f"Catched {count} from {name}. Remaining: {data[i]['pup_count']}"
                    }), 200
            else:
                data[i]["pup_count"] -= int(count)
                name = data[i]["pup_name"]

                ends = True

                out_res = jsonify({
                    "message": f"Not enough to catch {count}. Catched {data[i]['pup_count']}, ends."
                }), 200
    
    updated_data = data

    if(ends):
        updated_data = []
        for pup in data:
            if pup == out:
                continue
            updated_data.append(pup)  # Добавляем остальные записи

    with open("data/pupirky.json", 'w') as file:
        json.dump(updated_data, file, indent=4)

    # Если запись не найдена
    return out_res

@app.route('/pups/select/<string:name>', methods=['GET'])
def select_pup(name):
    count_f = 0
    data = json_read()

    for i in data:
        if(name == i["pup_name"]):
            count_f = 1
            out_res = jsonify({"message": f"Selected {i['pup_name']}, remaining: {i['pup_count']}"}), 200
            break

        if(name == i["pup_name"][:len(name)]):
            out_res = jsonify({"message": f"Selected {i['pup_name']}, remaining: {i['pup_count']}"}), 200
            count_f += 1

    if(count_f != 1):
        #print("Not found! Nothing be do.\n------------")
        return jsonify({"error": f"Pupiryshka '{name}' not found"}), 404

    return out_res

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Запуск сервера на всех интерфейсах