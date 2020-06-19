from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Event, EventGoer, Reward, Rewarder,RecommendedPerson
from accounts.models import Profile
from django.contrib.auth.models import User
import random

def eventPage(request,event_id):
    try:
        event = Event.objects.get(pk=event_id)
        context = {'event':event}
        return render(request,'system/eventpage.html',context)
    except Event.DoesNotExist:
        return redirect('/')

@login_required(login_url='/accounts/login')
def myPage(request,user_id):
    if request.user.id != user_id:
        return redirect('/accounts/login')
    else:
        try:
            print(request.META["REMOTE_ADDR"])
            user = User.objects.get(pk=user_id)
            rewards = Reward.objects.order_by('pointsNeeded')[:2]
            events_attending = EventGoer.objects.filter(user=user)
            profile = Profile.objects.get(user=user)
            for event in events_attending:
                event.recommend_link = 'localhost:8000/rew/e'+str(event.event.id)+'/'+str(user.id)
            if request.GET.get('msg'):
                message_to_display = request.GET.get('msg')
            else:
                message_to_display = None
            context = {'user':user,'profile':profile,'events_attending':events_attending,'rewards':rewards,'message':message_to_display}
            return render(request,'system/mypage.html',context)
        except User.DoesNotExist:
            return redirect('/accounts/registration')
        except Profile.DoesNotExist:
            profile = Profile()
            profile.user = user
            profile.save()
            if request.GET.get('msg'):
                message_to_display = request.GET.get('msg')
            else:
                message_to_display = None
            context = {'user':user,'profile':profile,'events_attending':events_attending,'message':message_to_display}
            return render(request,'system/mypage.html',context)

def recommendedEventPage(request,event_id,user_id):
    # When someone clicks the 'Register' button, he sends us form (POST)
    if request.method == 'POST':
        linkToRegister = request.POST['event_link']
        recommendor_id = request.POST['recommendor']
        #   --> We want to give a recommend-point to the recommender in our DB
        try:
            recommendor = User.objects.get(pk=recommendor_id)
            event = Event.objects.get(pk=event_id)
            eventGoer = EventGoer.objects.get(user=recommendor,event=event)
            print(request.META["REMOTE_ADDR"])
            # Create instance of this recommendor inviting this specific IP address = RecommendedPerson model
            recommendedPerson = RecommendedPerson.objects.filter(pk=request.META["REMOTE_ADDR"])
            if len(recommendedPerson) >= 1:
                return redirect(linkToRegister)
            else:
                newRecommendedPerson = RecommendedPerson.objects.create(pk=request.META["REMOTE_ADDR"],recommendor=eventGoer)
                newRecommendedPerson.save()
            eventGoer.numOfRecommended += 1
            eventGoer.save()
            #   --> Redirect the interested new guest to the event registration page (not on our rewardado page)
            return redirect(linkToRegister)
        except User.DoesNotExist:
            print("failure")
            return redirect(linkToRegister)
    else:
        if request.user.id == user_id:
            recommendorHerselfComingToThisPage = True
        else:
            recommendorHerselfComingToThisPage = False
        # If this is a valid recommendor link (recommendor with this id exists) and if the event exists then fine:
        try:
            recommendor = User.objects.get(pk=user_id)
            recommendedEvent = Event.objects.get(pk=event_id)
            context = {'recommendor':recommendor,'event':recommendedEvent,'recommendorHerselfComingToThisPage':recommendorHerselfComingToThisPage}
            return render(request,'system/eventpage.html',context)
        # If recommender_id or event_id is not found:
        except:
            return redirect('/')

@login_required(login_url='/accounts/login')
def myBuddies(request,user_id):
    if request.user.id != user_id:
        return redirect('/accounts/login')
    else:
        try:
            user = User.objects.get(pk=user_id)
            profile = Profile.objects.filter(user=user)
            events_attending = EventGoer.objects.filter(user=user)
            for event in events_attending:
                if event.eventBuddy == None:
                    try:
                        sameEventGoers = EventGoer.objects.filter(event=event.event).exclude(user=user)
                        if len(sameEventGoers) == 0: 
                            continue
                        pks = sameEventGoers.values_list('pk', flat=True)
                        random_idx = random.randint(0, len(pks) - 1)
                        while random_idx == int(event.id):
                            random_idx = random.randint(0, len(pks) - 1)
                        random_buddy = EventGoer.objects.get(pk=pks[random_idx])
                        event.eventBuddy = random_buddy
                        event.save()
                        if event.eventBuddy.eventBuddy == None:
                            event.eventBuddy.eventBuddy = event
                            event.eventBuddy.save()
                    except EventGoer.DoesNotExist:
                        continue
            context = {'user':user,'profile':profile,'events_attending':events_attending}
            return render(request,'system/mybuddies.html',context)
        except User.DoesNotExist:
            return redirect('/')
    return render(request,'system/mybuddies.html',context)


@login_required(login_url='/accounts/login')
def settingsPage(request,user_id):
    context = {}
    return render(request,'system/settingspage.html',context)

def eventlist(request):
    try:
        user = User.objects.get(pk=request.user.id)
        events = Event.objects.all()
        for event in events:
            eventAttending = EventGoer.objects.filter(user=user,event=event)
            if len(eventAttending) == 0:
                event.attending = False
            else:
                event.attending = True
        context = {'user':user,'events':events}
        return render(request,'system/eventlist.html',context)
    except User.DoesNotExist:
        return redirect('/')

@login_required(login_url='/accounts/login')
def getReward(request,rewID):
    try:
        reward = Reward.objects.get(pk=rewID)
        withdrawer = Profile.objects.get(user=request.user)
        print(withdrawer)
        if int(withdrawer.getPoints()) >= int(reward.pointsNeeded):
            reward_withdrawing = Rewarder()
            reward_withdrawing.withdrawer = withdrawer
            reward_withdrawing.reward = reward
            reward_withdrawing.save()
            return redirect("/rew/mypage/"+str(request.user.id)+"?msg=Your reward was successfully withdrawn! Expect an email from us with details :)")
        else:
            return redirect("/rew/mypage/"+str(request.user.id)+"?msg=You do not have enough credit")
    except Profile.DoesNotExist:
        print("No profile associated")
        return redirect('/')
    except Profile.MultipleObjectsReturned:
        print("More than one Profile object has been created")
        return redirect('/')
    #except:
        #print("Couldn't find the reward")
        #return redirect('/')
    return redirect('/rew/mypage/'+str(request.user.id))