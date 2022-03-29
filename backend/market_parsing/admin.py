from django.contrib import admin
from .models import GroupLink, Link, PriceLink, AnalogLink, AnalogLinkPrice

admin.site.register(GroupLink)
admin.site.register(Link)
admin.site.register(PriceLink)
admin.site.register(AnalogLink)
admin.site.register(AnalogLinkPrice)