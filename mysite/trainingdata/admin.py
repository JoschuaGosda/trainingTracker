from django.contrib import admin

# Register your models here.
from .models import Deadhang_max, Deadhang_endurance, Pullup_max, Pullup_endurance, Training, Leaderboard

admin.site.register(Deadhang_max)
admin.site.register(Deadhang_endurance)
admin.site.register(Pullup_max)
admin.site.register(Pullup_endurance)
admin.site.register(Training)
admin.site.register(Leaderboard)
