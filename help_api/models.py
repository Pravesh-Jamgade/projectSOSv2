from django.db import models
import uuid

# TYPE
STATUS = [("AE", "Active"), ("IE", "Inactive")]

TYPE = [("HL", "Hospital"), ("PN", "Person")]

TAG = [("BD", "Bed"), ("ONRL", "Oxygen Refill"), ("EYCR", "Empty Cylinder"),
       ("FLCR", "Full Cylinder"), ("NL", "NULL")]


class AddressModel(models.Model):
    entity_id = models.ForeignKey("EntityModel", on_delete=models.CASCADE)
    lane = models.CharField(("lane"), max_length=150, db_index=True)
    town = models.CharField(("town"), max_length=100, db_index=True)
    district = models.CharField(
        ("district"), max_length=100, db_index=True
    )
    state = models.CharField(("state"), max_length=100, db_index=True)
    contact_phone = models.CharField(max_length=10)
    contact_alternate_phone = models.CharField(max_length=10)
    email = models.EmailField("email", null=True, blank=True)


class EntityModel(models.Model):
    entity_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    entity_name = models.CharField(max_length=50)
    entity_type = models.CharField(max_length=3, choices=TYPE, default="PN")


class ToolsModel(models.Model):
    tool_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    tool_name = models.CharField(max_length=100)
    tool_from = models.ForeignKey("EntityModel", on_delete=models.PROTECT)
    tool_qty = models.IntegerField(blank=False, null=False)
    tool_state = models.CharField(max_length=3, choices=STATUS, default="IE")


class SOSModel(models.Model):
    sos_id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    sos_description = models.TextField(blank=False)
    sos_from = models.ForeignKey("EntityModel", models.PROTECT)
    sos_date = models.DateTimeField(auto_now=True)
    sos_state = models.CharField(max_length=3, choices=STATUS, default="IE")
    sos_tag = models.CharField(max_length=4, choices=TAG, default="NL")

# Create your models here.


# class UserModel(models.Model):
#     user_ph = models.CharField(max_length=10)
#     user_email = model.EmailField()
#     user_verified = model.BooleanField()
#     user_pass = model.CharField(max_length=10)
#     user_created_at = model.DateTimeField(auto_now=True)
