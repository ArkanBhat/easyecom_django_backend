from django.db import models


class WmsPartner(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    extra1 = models.CharField(max_length=255, null=True, blank=True)
    extra2 = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)

    class Meta:
        db_table = "wmspartner"

    def __str__(self):
        return self.name
    

class WmsPartnerApis(models.Model):
    partner = models.ForeignKey(WmsPartner, on_delete=models.CASCADE, related_name="apis")

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    curl = models.TextField(blank=True, null=True)
    apiurl = models.CharField(max_length=500)
    header = models.JSONField(blank=True, null=True)
    request = models.JSONField(blank=True, null=True)
    response = models.JSONField(blank=True, null=True)
    exception = models.TextField(blank=True, null=True)
    json = models.JSONField(blank=True, null=True)
    schema = models.JSONField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "wmspartnerapis"

    def __str__(self):
        return self.name    
    
class WmsCustomer(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, unique=True)
    type = models.CharField(max_length=100)
    extra1 = models.CharField(max_length=255, blank=True, null=True)
    extra2 = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "wmscustomer"

    def __str__(self):
        return self.name
    
class WmsCustomerAuth(models.Model):
    customer = models.ForeignKey(
        WmsCustomer,
        on_delete=models.CASCADE,
        related_name="auths"
    )

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    username = models.CharField(max_length=150)
    password = models.CharField(max_length=255)

    token = models.TextField(blank=True, null=True)
    key1 = models.CharField(max_length=255, blank=True, null=True)
    key2 = models.CharField(max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "wmscustomerauth"

    def __str__(self):
        return f"{self.name} - {self.customer.name}"



class ShipmentStatus(models.Model):
    code = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.code} - {self.name}"


class WmsShipments(models.Model):

    awb = models.CharField(max_length=255)
    order = models.CharField(max_length=255)

    customer = models.ForeignKey(
        WmsCustomer,
        on_delete=models.CASCADE,
        related_name='shipments'
    )

    request = models.TextField(blank=True, null=True)
    response = models.TextField(blank=True, null=True)
    exception = models.TextField(blank=True, null=True)

    status = models.ForeignKey(
    ShipmentStatus,
    on_delete=models.PROTECT,
    default=1
)
    is_active = models.BooleanField(default=True)

    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "wmsshipments"

    def __str__(self):
        return self.awb

class WmsShipmentLogs(models.Model):
    awb = models.CharField(max_length=255)
    order = models.CharField(max_length=255)

    error = models.TextField(blank=True, null=True)

    added_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = "wmsshipmentlogs"

    def __str__(self):
        return self.awb
    



