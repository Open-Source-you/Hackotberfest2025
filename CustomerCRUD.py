from flask import Flask, jsonify, request

app = Flask(__name__)

customers = []


@app.route("/customers", methods=["GET"])
def get_customers():
    return jsonify(customers)


@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):udidjeoeo
    customer = next((c for c in customers if c["id"] == customer_id), None)
    if customer:
        return jsonify(customer)
    return jsonify({"message": "Customer not found"}), 404


@app.route("/customers", methods=["POST"])
def add_customer():
    data = request.get_json()
    new_customer = {
        "id": len(customers) + 1,
        "name": data.get("name"),
        "email": data.get("email"),
        "phone": data.get("phone"),
        "address": data.get("address"),
    }
    customers.append(new_customer)
    return jsonify(new_customer), 201


@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = next((c for c in customers if c["id"] == customer_id), None)
    if not customer:
        return jsonify({"message": "Customer not found"}), 404
    data = request.get_json()
    customer["name"] = data.get("name", customer["name"])
    customer["email"] = data.get("email", customer["email"])
    customer["phone"] = data.get("phone", customer["phone"])
    customer["address"] = data.get("address", customer["address"])
    return jsonify(customer)


@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    global customers
    customers = [c for c in customers if c["id"] != customer_id]
    return jsonify({"message": "Customer deleted"})


if __name__ == "__main__":
    app.run(debug=True)
