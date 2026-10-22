from django.contrib import admin

from django.contrib import admin
from .models import (Ambalaj, Categorie, Brand, SediuCompanie, DepozitSediu,
                     ServiciuAditional, CompaniePartenera, Produs
)
admin.site.register(Ambalaj)
admin.site.register(Categorie)
admin.site.register(Brand)
admin.site.register(SediuCompanie)
admin.site.register(DepozitSediu)
admin.site.register(ServiciuAditional)
admin.site.register(CompaniePartenera)
admin.site.register(Produs)
# Register your models here.
