from django.db import models
from django.contrib.auth.models import User
from system.models import EventGoer

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
    def getPoints(self):
        eventsGoingTo = EventGoer.objects.filter(user=self.user)
        # We give 3 points as a headstart for our users
        pointsSum = 3
        for event in eventsGoingTo:
            pointsSum += event.numOfRecommended
        return pointsSum