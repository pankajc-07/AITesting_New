from flask import Blueprint, request, jsonify
from models import db, Customer

customers_bp = Blueprint("customers", __name__)


@customers_bp.route("/api/customers", methods=["GET"])
def get_customers():
    search = request.args.get("search", "")
    query = Customer.query
    if search:
        query = query.filter(
            Customer.name.ilike(f"%{search}%") | Customer.phone.ilike(f"%{search}%")
        )
    customers = query.order_by(Customer.name).all()
    return jsonify([c.to_dict() for c in customers])


@customers_bp.route("/api/customers/<int:customer_id>", methods=["GET"])
def get_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return jsonify(customer.to_dict())


@customers_bp.route("/api/customers", methods=["POST"])
def create_customer():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("phone"):
        return jsonify({"error": "Name and phone are required"}), 400

    existing = Customer.query.filter_by(phone=data["phone"]).first()
    if existing:
        return jsonify({"error": "Customer with this phone number already exists"}), 409

    customer = Customer(
        name=data["name"],
        phone=data["phone"],
        email=data.get("email"),
        address=data.get("address"),
    )
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_dict()), 201


@customers_bp.route("/api/customers/<int:customer_id>", methods=["PUT"])
def update_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    data = request.get_json()

    if "name" in data:
        customer.name = data["name"]
    if "phone" in data:
        existing = Customer.query.filter(Customer.phone == data["phone"], Customer.id != customer_id).first()
        if existing:
            return jsonify({"error": "Customer with this phone number already exists"}), 409
        customer.phone = data["phone"]
    if "email" in data:
        customer.email = data["email"]
    if "address" in data:
        customer.address = data["address"]

    db.session.commit()
    return jsonify(customer.to_dict())


@customers_bp.route("/api/customers/<int:customer_id>", methods=["DELETE"])
def delete_customer(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    db.session.delete(customer)
    db.session.commit()
    return jsonify({"message": "Customer deleted successfully"}), 200