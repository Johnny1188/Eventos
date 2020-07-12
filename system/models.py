from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import redirect
import hashlib
import random
import datetime


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    linkToRegister = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images/',default='event_images/event_placeholder.png')
    def __str__(self):
        return self.name
    class Meta:
        ordering = ["-date"]

class EventGoer(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    eventBuddy = models.OneToOneField('EventGoer', on_delete=models.SET_NULL, null=True, blank=True)
    chatName = models.CharField(max_length=120,default='',null=True, blank=True)
    numOfRecommended = models.IntegerField(default=0)
    def __str__(self):
        return self.event.name[:15] + "---" + self.user.username
    def getChat(self):
        if self.chatName == '':
            roomChatName = hashlib.md5((self.event.name + self.eventBuddy.user.username).encode()).hexdigest()
            self.eventBuddy.chatName = roomChatName
            self.chatName = roomChatName
            super().save()
            self.eventBuddy.save()
            print(self.chatName)
            return self.chatName
        else:
            return self.chatName

class Reward(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(max_length=1000)
    quantity = models.IntegerField(default=0)
    pointsNeeded = models.IntegerField(default=1)
    image = models.ImageField(upload_to='rewards_images/',default='rewards_images/reward_placeholder.svg')
    def __str__(self):
        return self.name[:15]

# Model for admins to see which rewards wants to be withdrawn
#   - admins will see all objects so that they know which and to whom to fulfill the reward withdraw
class RewardWithdrawer(models.Model):
    withdrawer = models.ForeignKey('accounts.Profile',on_delete=models.CASCADE)
    reward = models.ForeignKey(Reward,on_delete=models.SET_NULL,null=True,blank=True)
    fulfilled = models.BooleanField(default=False)
    def __str__(self):
        return str(self.withdrawer.id) + '---' + str(self.reward.id) + '---' + str(self.fulfilled)

class Message(models.Model):
    text = models.TextField()
    chatName = models.CharField(max_length=255)
    sender = models.ForeignKey(User,on_delete=models.CASCADE)
    timeSent = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    def __str__(self):
        return str(self.id)

class RecommendedPerson(models.Model):
    ipAddress = models.CharField(max_length=60, primary_key=True)
    recommendor = models.ForeignKey("Eventgoer",on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    def __str__(self):
        return self.recommendor.user.username + '---' + self.ipAddress + '---' + str(self.timestamp)


