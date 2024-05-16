from django.contrib import admin

from .models import USERS
admin.site.register(USERS)
from .models import CATEGORY
admin.site.register(CATEGORY)
