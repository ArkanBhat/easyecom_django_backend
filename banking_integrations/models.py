from django.db import models

class UPITransaction(models.Model):
    merchant_tran_id = models.CharField(max_length=35, unique=True)
    ref_id = models.CharField(max_length=50, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="PENDING")
    bank_rrn = models.CharField(max_length=30, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.merchant_tran_id

class RefundTransaction(models.Model):
    merchant_tran_id = models.CharField(max_length=35)
    original_merchant_tran_id = models.CharField(max_length=35)
    original_bank_rrn = models.CharField(max_length=30, null=True, blank=True)
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.merchant_tran_id
