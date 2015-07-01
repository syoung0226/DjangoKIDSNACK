from food.models import Category, Snack, SideEffect, Additive, GovernmentSnack, SnackHate, SnackLike, RawMaterial, RequireSnack
from django.contrib import admin

# Register your models here.


admin.site.register(Category)
admin.site.register(Snack)
admin.site.register(SideEffect)
admin.site.register(Additive)
admin.site.register(GovernmentSnack)
admin.site.register(RawMaterial)
admin.site.register(SnackHate)
admin.site.register(SnackLike)
admin.site.register(RequireSnack)