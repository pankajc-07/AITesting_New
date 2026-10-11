from datetime import date

from flask import Blueprint, request, jsonify
from models import db, MedicineRecord, Customer

medicines_bp = Blueprint("medicines", __name__)


@medicines_bp.route("/api/customers/<int:customer_id>/medicines", methods=["GET"])
def get_medicines(customer_id):
    Customer.query.get_or_404(customer_id)
    medicines = MedicineRecord.query.filter_by(customer_id=customer_id).order_by(MedicineRecord.date_purchased.desc()).all()
    return jsonify([m.to_dict() for m in medicines])


@medicines_bp.route("/api/customers/<int:customer_id>/medicines", methods=["POST"])
def add_medicine(customer_id):
    Customer.query.get_or_404(customer_id)
    data = request.get_json()
    if not data or not data.get("medicine_name"):
        return jsonify({"error": "Medicine name is required"}), 400

    date_str = data.get("date_purchased")
    if date_str:
        date_purchased = date.fromisoformat(date_str)
    else:
        date_purchased = date.today()

    medicine = MedicineRecord(
        customer_id=customer_id,
        medicine_name=data["medicine_name"],
        dosage=data.get("dosage"),
        quantity=data.get("quantity", 1),
        date_purchased=date_purchased,
        notes=data.get("notes"),
    )
    db.session.add(medicine)
    db.session.commit()
    return jsonify(medicine.to_dict()), 201


@medicines_bp.route("/api/medicines/<int:medicine_id>", methods=["PUT"])
def update_medicine(medicine_id):
    medicine = MedicineRecord.query.get_or_404(medicine_id)
    data = request.get_json()

    if "medicine_name" in data:
        medicine.medicine_name = data["medicine_name"]
    if "dosage" in data:
        medicine.dosage = data["dosage"]
    if "quantity" in data:
        medicine.quantity = data["quantity"]
    if "date_purchased" in data:
        medicine.date_purchased = date.fromisoformat(data["date_purchased"])
    if "notes" in data:
        medicine.notes = data["notes"]

    db.session.commit()
    return jsonify(medicine.to_dict())


@medicines_bp.route("/api/medicines/<int:medicine_id>", methods=["DELETE"])
def delete_medicine(medicine_id):
    medicine = MedicineRecord.query.get_or_404(medicine_id)
    db.session.delete(medicine)
    db.session.commit()
    return jsonify({"message": "Medicine record deleted successfully"}), 200