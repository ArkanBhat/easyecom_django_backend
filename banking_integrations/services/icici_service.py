import uuid
from banking_integrations.models import UPITransaction
from banking_integrations.services.encryption_service import hybrid_encrypt


class ICICIService:

    @staticmethod
    def generate_qr(amount):
        merchant_tran_id = uuid.uuid4().hex

        payload = {
            "merchantTranId": merchant_tran_id,
            "amount": amount,
            "currency": "INR"
        }

        encrypted_data = hybrid_encrypt(payload)

        transaction = UPITransaction.objects.create(
            merchant_tran_id=merchant_tran_id,
            amount=amount,
            status="PENDING"
        )

        return {
            "message": "QR request created",
            "merchant_tran_id": merchant_tran_id,
            "encrypted_request": encrypted_data
        }
