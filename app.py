from flask import Flask, jsonify, request

app = Flask(__name__)


items = [
    {"id": 1, "name": "item1", "price": 10},
    {"id": 2, "name": "item2", "price": 20},
    {"id": 3, "name": "item3", "price": 30},
]


@app.route("/")
def home():
    return "welcome to the home page"


##get request
@app.route("/items", methods=["GET"])
def get_items():
    return jsonify(items)


# get request for single item
@app.route("/items/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "item not found"}), 404


# post request for creating new item
@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json()
    new_item = {"id": len(items) + 1, "name": data["name"], "price": data["price"]}
    items.append(new_item)
    return jsonify(new_item), 200


# put request for updating item
@app.route("/items/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = next((item for item in items if item["id"] == item_id), None)
    if item is None:
        return jsonify({"error": "no item found"})
    item["name"] = request.json.get("name", item["name"])
    item["price"] = request.json.get("price", item["price"])

    return jsonify(item)


# delete request for deleting item
@app.route("/items/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    global items
    items = [item for item in items if item["id"] != item_id]
    return jsonify({"result": "item deleted"})


if __name__ == "__main__":
    app.run(debug=True)
