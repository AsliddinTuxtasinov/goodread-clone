from django.contrib import admin
from auusers.models import CostumUser


@admin.register(CostumUser)
class CostumUserAdmin(admin.ModelAdmin):
    pass
