from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile
from system.models import EventGoer,Event
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

def registration(request):
    if request.method == 'POST':
        if request.POST['email'] and request.POST['password1'] and request.POST['password2']:
            if request.POST['password1'] == request.POST['password2']:
                try:
                    # Check whether the user is already registered:
                    user = User.objects.get(username=request.POST['email'])
                    try:
                        try:
                            event_id = int(request.GET['event'])
                        except:
                            event_id = int(request.POST['event_id_from_newcollector'])
                        event = Event.objects.get(pk=event_id)
                        eventGoer = EventGoer.objects.filter(event=event,user=user)
                        # User exists but the EventGoer instance does not -> let him login and create the instance
                        if len(eventGoer) == 0:
                            return redirect('/accounts/login?event=' + str(event_id) + '&error=Use your already existing account')
                        else:
                            return render(request, 'accounts/login.html')
                    except:
                        pass
                    return render(request, 'accounts/registration.html', {'error':'This email is already connected to an account'})
                except User.DoesNotExist:
                    user = User.objects.create_user(request.POST['email'], password=request.POST['password1'])
                    # If this link to registration came through email ticket
                    #    ---> needs to have url parameters (?event=event_id)
                    try:
                        try:
                            event_id = int(request.GET['event'])
                        except:
                            event_id = int(request.POST['event_id_from_newcollector'])
                        try:
                            event = Event.objects.get(pk=event_id)
                        except:
                            return redirect('/accounts/registration')
                        if event:
                            eventGoer = EventGoer.objects.filter(event=event,user=user)
                            if len(eventGoer) == 0:
                                newEventGoer = EventGoer()
                                newEventGoer.event = event
                                newEventGoer.user = user
                                newEventGoer.save()
                    # If it is basic /accounts/registration url --> then we don't care about eventGoer model:
                    except:
                        pass
                    # Finish setting up user's profile:
                    user_profile = Profile()
                    user_profile.user = user
                    user_profile.email = request.POST['email']
                    user_profile.save()
                    auth.login(request,user)
                    return redirect('/rew/mypage/'+str(user.id))
            else:
                try:
                    error = request.POST['event_id_from_newcollector']
                    return redirect('/rew/newrewardcollector/1?error=Passwords must match')
                except:
                    return render(request, 'accounts/registration.html', {'error':'Passwords must match'})
        else:
            try:
                error = request.POST['event_id_from_newcollector']
                return redirect('/rew/newrewardcollector/1?error=All fields must be filled')
            except:
                return render(request, 'accounts/registration.html', {'error':'All fields must be filled'})
    else:
        context = {}
        try:
            isItEventReg = request.GET["event"]
            context = {'eventHeadline':'To collect your rewards, please sign up with your email address:'}
        except:
            pass
        return render(request, 'accounts/registration.html', context)

def login(request):
    if request.method == 'POST':
        if request.POST['email'] and request.POST['password1']:
            user = auth.authenticate(username=request.POST['email'], password=request.POST['password1'])
            if user is not None:
                try:
                    event_id = int(request.GET["event"])
                    event = Event.objects.get(pk=event_id)
                    eventGoer = EventGoer.objects.filter(event=event,user=user)
                    if len(eventGoer) == 0:
                        newEventGoer = EventGoer()
                        newEventGoer.event = event
                        newEventGoer.user = user
                        newEventGoer.save()
                except:
                    pass
                auth.login(request, user)
                return redirect('/rew/mypage/'+str(user.id))
            else:
                return render(request, 'accounts/login.html', {'error': 'Password or email is incorrect'})
        else:
            return render(request, 'accounts/login.html', {'error':'You must fill all fields'})
    else:
        try:
            msg = request.GET["error"]
            context = {"message":msg}
        except:
            context = {}
            pass
        return render(request, 'accounts/login.html', context)

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('/')
    else:
        return render(request, 'accounts/login.html', {'error': 'Some technical flaw, sorry for that'})

@login_required(login_url='/accounts/login')
def deleteAccount(request,userid):
    try:
        user = User.objects.get(pk=userid)
        if request.user == user:
            user.delete()
            return redirect('/')
        else:
            return redirect('/accounts/login')
    except:
        return redirect('/accounts/registration')