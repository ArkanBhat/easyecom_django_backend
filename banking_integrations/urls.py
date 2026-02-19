from django.urls import path
from .views import generate_qr, icici_callback, transaction_status, callback_status,refund, simulate_bank_callback

urlpatterns = [
    path("generate-qr/", generate_qr),
    path("callback/", icici_callback),
    path("transaction-status/", transaction_status),
    path("callback-status/", callback_status),
    path("refund/", refund),
    path("simulate-bank/", simulate_bank_callback),

]
