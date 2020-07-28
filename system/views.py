from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Event, EventGoer, Reward, RewardWithdrawer,RecommendedPerson,Message
from accounts.models import Profile
from django.contrib.auth.models import User
import datetime
import random
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from .tasks import sendEmail

def eventPage(request,event_id):
    try:
        event = Event.objects.get(pk=event_id)
        #    LOGIC TO SEND INFO ABOUT THE USER WHETHER HE HAS REGISTERED FOR THE SPECIFIC EVENT:
        if request.user.is_authenticated == False:
           is_registered = False
        else:
            eventGoer = EventGoer.objects.filter(event=event,user=request.user)
            if len(eventGoer) == 0:
                is_registered = False
            else:
                is_registered = True
        context = {'event':event, 'is_registered':is_registered}
        return render(request,'system/eventpage.html',context)
    except Event.DoesNotExist:
        return redirect('/')

def newRewardCollector(request,event_id):
    try:
        event = Event.objects.get(pk=event_id)
        rewards = Reward.objects.order_by('pointsNeeded')
        try:
            error_msg = request.GET['error']
            context = {'event':event,'rewards':rewards,'error':error_msg}
            to_render = render(request,'system/newcollector.html',context)
            to_render.set_cookie("eventid",event_id)
            return to_render
        except:
            context = {'event':event,'rewards':rewards}
            to_render = render(request,'system/newcollector.html',context)
            to_render.set_cookie("eventid",event_id)
            return to_render
    except:
        return redirect('/')

@login_required(login_url='/accounts/login')
def myPage(request,user_id):
    # OAuth -> 'cross-site':
    if request.META['HTTP_SEC_FETCH_SITE'] == 'cross-site':
        oauth_user = DefaultSocialAccountAdapter()
        oauth_user.new_user(oauth_user, request)
        request.user.username = request.user.email
        request.user.save()
    if request.user.id != user_id:
        return redirect('/accounts/login')
    else:
        try:
            user = User.objects.get(pk=user_id)
            rewards = Reward.objects.order_by('pointsNeeded')
            profile = Profile.objects.get(user=user)
        except User.DoesNotExist:
            return redirect('/accounts/signup')
        except Profile.DoesNotExist:
            profile = Profile()
            profile.user = user
            profile.save()
        except Reward.DoesNotExist:
            rewards = None
        # Find out which rewards have already been withdrawn by this user:
        withdrawnrewards = RewardWithdrawer.objects.filter(withdrawer=profile)
        for reward in rewards:
            if RewardWithdrawer.objects.filter(withdrawer=profile,reward=reward).exists():
                reward.alreadyWithdrawn = True
        events_attending = EventGoer.objects.filter(user=user)
        for event in events_attending:
            event.recommend_link = 'localhost:8000/rew/e'+str(event.event.id)+'/'+str(user.id)
        if request.GET.get('msg'):
            message_to_display = request.GET.get('msg')
        else:
            message_to_display = None
        context = {'user':user,'profile':profile,'events_attending':events_attending,'rewards':rewards,'message':message_to_display}
        return render(request,'system/mypage.html',context)

def recommendedEventPage(request,event_id,user_id):
    # When someone clicks the 'Register' button, he sends us form (POST)
    if request.method == 'POST':
        linkToRegister = request.POST['event_link']
        recommendor_id = request.POST['recommendor']
        #   --> We want to give a recommend-point to the recommender in our DB
        try:
            print("Celeryy gooo!")
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
            print("Celeryy gooo!")
            # Send email saying that the person invited someone successfuly and received 1 credit (Celery Job):
            send_email = sendEmail.delay(user_id)
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
            events_attending = EventGoer.objects.filter(user=user)
            for event in events_attending:
                if event.eventBuddy == None:
                    try:
                        sameEventGoers = EventGoer.objects.filter(event=event.event,eventBuddy=None).exclude(user=user)
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
            context = {'user':user,'events_attending':events_attending}
            return render(request,'system/mybuddies.html',context)
        except User.DoesNotExist:
            return redirect('/')
    return render(request,'system/mybuddies.html',context)


@login_required(login_url='/accounts/login')
def settingsPage(request,user_id):
    if request.user.id != user_id:
        return redirect('/accounts/login')
    else:
        user = request.user
        try:
            profile_with_preferences = Profile.objects.get(user=user)
            context = {'profile':profile_with_preferences}
        except Profile.DoesNotExist:
            auth.logout(request)
            return redirect('/accounts/login')
        return render(request,'system/settingspage.html',context)

@login_required(login_url='/accounts/login')
def changePreference(request):
    try:
        profile = Profile.objects.get(user__id=request.POST['userid'])
        preferenceToChange = request.POST['preference_to_change']
        turnPreference = request.POST['turn']
        if preferenceToChange == "sendCreditInfo":
            if turnPreference == "on":
                profile.sendCreditInfo = True
            else:
                profile.sendCreditInfo = False
        if preferenceToChange == "sendEventUpdates":
            if turnPreference == "on":
                profile.sendEventUpdates = True
            else:
                profile.sendEventUpdates = False
        profile.save()
        data = {
                'message': "Successfully changed the preference."
            }
        return JsonResponse(data)
    except:
        return redirect('/accounts/login')

def eventlist(request):
    try:
        print(datetime.datetime.now())
        user = User.objects.get(pk=request.user.id)
        events = Event.objects.filter(date__gt=datetime.datetime.now()).order_by('date')
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
        if int(withdrawer.getPoints()) >= int(reward.pointsNeeded):
            if int(reward.quantity) < 1:
                return redirect("/rew/mypage/"+str(request.user.id)+"?msg=Error")
            else:
                reward.quantity -= 1
                reward.save()
                reward_withdrawing = RewardWithdrawer()
                reward_withdrawing.withdrawer = withdrawer
                reward_withdrawing.reward = reward
                reward_withdrawing.save()
                return redirect("/rew/mypage/"+str(request.user.id)+"?msg=Success")
        else:
            return redirect("/rew/mypage/"+str(request.user.id)+"?msg=Fail")
    except Profile.DoesNotExist:
        print("No profile associated")
        return redirect('/')
    except Profile.MultipleObjectsReturned:
        print("More than one Profile object has been created")
        return redirect('/')
    except:
        print("Couldn't find the reward")
        return redirect('/')
    return redirect('/rew/mypage/'+str(request.user.id))

@login_required(login_url='/accounts/login')
def ajaxGetOlderMessages(request):
    messagesToReturn = {'messages':[]}
    try:
        chat_name = request.GET["name"]
        message_batch_number = request.GET["batch"]
        interval_of_messages_to_load = [(20*(int(message_batch_number)-1)),(20*(int(message_batch_number)))]
        messages = Message.objects.filter(chatName='chat_'+chat_name).order_by('-id')[interval_of_messages_to_load[0]:interval_of_messages_to_load[1]].values('id','text','sender')
        for message in messages:
            messagesToReturn['messages'].append({'sender':message['sender'],'text':message['text']})
    except:
        messagesToReturn['messages'].append({'sender':'system','text':'Failed to load messages'})
    return JsonResponse(messagesToReturn)
