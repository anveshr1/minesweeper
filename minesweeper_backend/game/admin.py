from django.contrib import admin

# Register your models here.
from .models.game import Game

admin.site.register(Game)
