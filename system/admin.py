from django.contrib import admin
from .models import Event,EventGoer,Reward,Rewarder,Message,RecommendedPerson

admin.site.register(Event)
admin.site.register(EventGoer)
admin.site.register(Reward)
admin.site.register(Rewarder)
admin.site.register(Message)
admin.site.register(RecommendedPerson)