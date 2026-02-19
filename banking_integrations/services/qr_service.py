import json
import uuid

def generate_merchant_tran_id():
    return str(uuid.uuid4()).replace("-", "")[:30]


def build_qr_payload(amount):
    merchant_tran_id = generate_merchant_tran_id()

    payload = {
        "merchantId": "YOUR_MERCHANT_ID",
        "terminalId": "5411",
        "amount": f"{amount:.2f}",
        "merchantTranId": merchant_tran_id,
        "billNumber": merchant_tran_id
    }

    return payload, merchant_tran_id
