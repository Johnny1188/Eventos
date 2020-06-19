from django_cron import CronJobBase, Schedule
from .models import RecommendedPerson
from django.utils import timezone
import time
import datetime

# Cron task management:
class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 0.01 # test 1 minute
    #RUN_EVERY_MINS = 960 # every 16 hours
    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'Recommended_people_deletion'
    def do(self):
        oldRecommendedPeopleInstances = RecommendedPerson.objects.all()
        for instance in oldRecommendedPeopleInstances:
            # If the instance is older than two months delete it from the database:
            if int(instance.timestamp.month) + 2 <= int(datetime.datetime.now().month):
                instance.delete()

