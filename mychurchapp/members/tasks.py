from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_newsletter_email(subject, message, email):
    send_mail(
        subject,
        message,
        'HOST_EMAIL',  # Replace with your email
        [email],
    )


from django.utils import timezone
from .models import ChurchMember, Newsletter

@shared_task
def check_member_status_and_send_emails():
    # Send emails to inactive members
    inactive_members = ChurchMember.objects.filter(is_inactive=True)
    for member in inactive_members:
        newsletter = Newsletter.objects.get(subject='Inactive Member')
        send_newsletter_email.delay(newsletter.subject, newsletter.content, member.email)
    
    # Send emails to new members
    new_members = ChurchMember.objects.filter(date_joined=timezone.now().date())
    for member in new_members:
        newsletter = Newsletter.objects.get(subject='New Member')
        send_newsletter_email.delay(newsletter.subject, newsletter.content, member.email)

    # Send emails to first time attendees
    first_time_attendees = ChurchMember.objects.filter(churchattendancerecord__service_type='SUN')
    for member in first_time_attendees:
        if member.date_joined == timezone.now().date():
            newsletter = Newsletter.objects.get(subject='Thank You')
            send_newsletter_email.delay(newsletter.subject, newsletter.content, member.email)
