from django.core.mail import EmailMultiAlternatives, send_mail
from accounts.models import Profile
from django.conf import settings

def send_custom_email(what_happened, recipient):
    try:
        user_preferences = Profile.objects.get(user=recipient)
        # Check whether she wants to get updates on her credit:
        #       If the what_happened is not about credit, then stop it
        if what_happened == "New credit received, withdraw your rewards":
            if user_preferences.sendCreditInfo == False:
                raise NameError("User does not want to send emails about credits")
        else:
            raise NameError("Wanted to send some nasty email but my big brain stopped it!")
        text_content = "Hi, we just wanted to let you know that someone accepted your invitation to the Startup Disrupt event and you got +1 credit. Take a look, whether you can withdraw some reward here: reward.startupdisrupt.com/accounts/login"
        html_content = "<p>Hi, we just wanted to let you know that someone accepted your invitation to the Startup Disrupt event and you got +1 credit. Take a look, whether you can withdraw some reward here: <a href='reward.startupdisrupt.com/accounts/login'>reward.startupdisrupt.com</a></p>  <br>  <br>  <br>  <br>  <br>  <br> <p style='color: gray;font-size: 9px;text-align: center;'>If you no longer wish to receive these emails, please login <a href='reward.startupdisrupt.com/accounts/login'>here</a>, go to settings and turn off your notifications.</p>"
        msg = EmailMultiAlternatives(what_happened, text_content,settings.EMAIL_HOST_USER,[recipient.username])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        #send_mail(what_happened,
        #        'Hi, we just wanted to let you know that someone accepted your invitation to the Startup Disrupt event and you got +1 credit. Sign in and take a look, whether you can withdraw some reward: reward.startupdisrupt.com/accounts/login',
        #        settings.EMAIL_HOST_USER,
        #        [recipient.username],)
    except Profile.DoesNotExist:
        send_mail("EVENTOS: Profile not found",
                'Eventos wanted to send email to user but could not find her Profile (preferences).',
                settings.EMAIL_HOST_USER,
                ["jsobotka@centrum.cz"],)
    except NameError as err:
        send_mail("EVENTOS: Something wrong in send_custom_email()",
                str(err),
                settings.EMAIL_HOST_USER,
                ["jsobotka@centrum.cz"],)
