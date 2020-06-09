from django.contrib import admin
from .models import Event,EventGoer,Reward,Rewarder

admin.site.register(Event)
admin.site.register(EventGoer)
admin.site.register(Reward)
admin.site.register(Rewarder)