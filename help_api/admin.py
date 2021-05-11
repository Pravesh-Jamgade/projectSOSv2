from django.contrib import admin
from help_api.models import (
    AddressModel, EntityModel, ToolsModel,
    SOSModel
)
# Register your models here.
admin.site.register(AddressModel)
admin.site.register(EntityModel)
admin.site.register(ToolsModel)
admin.site.register(SOSModel)
