import os
import requests
from flask import Flask, Blueprint, request, jsonify

app = Flask(__name__)

# LEVEL 3 (HARD): Flask Blueprint with url_prefix
billing_bp = Blueprint("billing_module", __name__, url_prefix="/api/v1/billing")

ORDER_SERVICE_WEBHOOK_URL = os.getenv("ORDER_WEBHOOK_URL", "http://order-service:3000/api/v1/webhooks/payment-callback")

@billing_bp.route("/charge", methods=["POST"])
def charge():
    """
    Full path: POST /api/v1/billing/charge
    Matches BillingServiceClient.charge_customer() in repo_1.
    And initiates a REVERSE CROSS-REPO CALL to repo_1 Webhook!
    """
    data = request.get_json() or {}
    order_id = data.get("order_id", "unknown")
    amount = data.get("amount", 0.0)

    txn_id = f"txn_{os.urandom(4).hex()}"

    # REVERSE CALL: repo_2 calling repo_1 webhook!
    send_webhook_to_repo_1(order_id, txn_id, "PAID")

    return jsonify({
        "status": "charged",
        "transaction_id": txn_id,
        "amount": amount,
        "order_id": order_id
    }), 200

@billing_bp.route("/invoices/<invoice_id>", methods=["GET"])
def get_invoice(invoice_id):
    """
    LEVEL 2 (MEDIUM): Flask parameter style <invoice_id>
    Matches repo_1 BillingServiceClient.get_invoice_async()
    """
    return jsonify({
        "invoice_id": invoice_id,
        "status": "SETTLED",
        "tax": 10.5
    }), 200

def send_webhook_to_repo_1(order_id: str, transaction_id: str, status: str):
    """
    LEVEL 3 (BIDIRECTIONAL CROSS-REPO LINK):
    Repo 2 calling repo 1's Express webhook:
    POST http://order-service:3000/api/v1/webhooks/payment-callback
    """
    try:
        requests.post(
            ORDER_SERVICE_WEBHOOK_URL,
            json={"orderId": order_id, "transactionId": transaction_id, "status": status},
            timeout=3.0
        )
    except Exception as e:
        print(f"[Warning] Failed to send webhook callback: {e}")

# Register Blueprint
app.register_blueprint(billing_bp)
