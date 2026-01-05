from django.contrib import admin
from .models import Bike, Part, Service, BlogPost, OwnersGroupPost

admin.site.register(Bike)
admin.site.register(Part)
admin.site.register(Service)
admin.site.register(BlogPost)
admin.site.register(OwnersGroupPost)
