from django.contrib import admin

from .models import Insuranceplan, InsuranceplanFile


class InsuranceplanFileInline(admin.TabularInline):
    model = InsuranceplanFile
    extra = 1


class InsuranceplanAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'slug', 'is_digital']
    inlines = [InsuranceplanFileInline]
    class Meta:
        model = Insuranceplan

admin.site.register(Insuranceplan, InsuranceplanAdmin)