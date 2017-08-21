#from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Profile,Marks_card,Vote

admin.site.register(Profile)
admin.site.register(Marks_card)
admin.site.register(Vote)
