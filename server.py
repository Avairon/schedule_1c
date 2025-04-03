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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Запуск сервера на всех интерфейсах