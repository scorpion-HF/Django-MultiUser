from django.contrib import admin
from users.models import CustomUser, SupervisorProfile, NormalProfile

admin.site.register(CustomUser)
admin.site.register(SupervisorProfile)
admin.site.register(NormalProfile)
