from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .services.encryption_service import hybrid_encrypt
from .models import UPITransaction
from .services.qr_service import build_qr_payload
from .services.encryption_service import hybrid_encrypt
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.Util.Padding import unpad
from Crypto.PublicKey import RSA
import base64
from .services.qr_service import generate_merchant_tran_id
from .models import UPITransaction, RefundTransaction
from .services.encryption_service import hybrid_decrypt


@csrf_exempt
def generate_qr(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            amount = float(data.get("amount"))

            # Build payload
            payload, merchant_tran_id = build_qr_payload(amount)
            encrypted_payload = hybrid_encrypt(payload)

            # Save in DB
            transaction = UPITransaction.objects.create(
                merchant_tran_id=merchant_tran_id,
                amount=amount,
                status="PENDING"
            )

            return JsonResponse({
                "message": "QR request created",
                "merchant_tran_id": merchant_tran_id,
                "encrypted_request": encrypted_payload
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)


@csrf_exempt
def icici_callback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            decrypted_payload = hybrid_decrypt(
                data.get("encryptedKey"),
                data.get("iv"),
                data.get("encryptedData")
            )

            print("Decrypted callback:", decrypted_payload)

            merchant_tran_id = decrypted_payload.get("merchantTranId")
            status = decrypted_payload.get("status")
            bank_rrn = decrypted_payload.get("BankRRN")

            transaction = UPITransaction.objects.filter(
                merchant_tran_id=merchant_tran_id
            ).first()

            if transaction:
                transaction.status = status
                transaction.bank_rrn = bank_rrn
                transaction.save()

            return JsonResponse({"message": "Callback processed"})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)


@csrf_exempt
def transaction_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            merchant_tran_id = data.get("merchantTranId")

            transaction = UPITransaction.objects.filter(
                merchant_tran_id=merchant_tran_id
            ).first()

            if not transaction:
                return JsonResponse({"error": "Transaction not found"}, status=404)

            return JsonResponse({
                "merchantTranId": transaction.merchant_tran_id,
                "amount": str(transaction.amount),
                "status": transaction.status,
                "bankRRN": transaction.bank_rrn
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)

@csrf_exempt
def callback_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            merchant_tran_id = data.get("merchantTranId")
            bank_rrn = data.get("BankRRN")
            ref_id = data.get("refID")

            transaction = None

            if merchant_tran_id:
                transaction = UPITransaction.objects.filter(
                    merchant_tran_id=merchant_tran_id
                ).first()

            elif bank_rrn:
                transaction = UPITransaction.objects.filter(
                    bank_rrn=bank_rrn
                ).first()

            elif ref_id:
                transaction = UPITransaction.objects.filter(
                    ref_id=ref_id
                ).first()

            if not transaction:
                return JsonResponse({"error": "Record not found"}, status=404)

            return JsonResponse({
                "merchantTranId": transaction.merchant_tran_id,
                "amount": str(transaction.amount),
                "status": transaction.status,
                "bankRRN": transaction.bank_rrn,
                "success": transaction.status == "SUCCESS"
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)

@csrf_exempt
def refund(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            original_tran_id = data.get("originalMerchantTranId")
            refund_amount = float(data.get("refundAmount"))

            original_transaction = UPITransaction.objects.filter(
                merchant_tran_id=original_tran_id
            ).first()

            if not original_transaction:
                return JsonResponse({"error": "Original transaction not found"}, status=404)

            refund_tran_id = generate_merchant_tran_id()

            refund_obj = RefundTransaction.objects.create(
                merchant_tran_id=refund_tran_id,
                original_merchant_tran_id=original_tran_id,
                original_bank_rrn=original_transaction.bank_rrn,
                refund_amount=refund_amount,
                status="PENDING"
            )

            return JsonResponse({
                "refundTranId": refund_tran_id,
                "status": refund_obj.status
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)

@csrf_exempt
def simulate_bank_callback(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            encrypted = hybrid_encrypt(data)

            return JsonResponse(encrypted)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=405)
