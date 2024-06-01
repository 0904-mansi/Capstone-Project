# signals.py

from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from employee.models import Employee, Manager

@receiver(post_save, sender=Employee)
def send_employee_details_email(sender, instance, created, **kwargs):
    if created:
        # Compose the email content using the template
        email_subject = 'Here are Your Credentials for Login to Employee Portal : {}'.format(instance.firstName)
        email_body = 'Employee Name: {}\nEmployee Email: {}\n'.format(instance.firstName, instance.email)+f'Employee ID : {instance.eID}\n' 
        
        # Send the email
        send_mail(
            email_subject,
            email_body,
            'mansimishra510@gmail.com',  # Sender's email address
            ['mansimishra2314@gmail.com'],  # Recipient's email address
            fail_silently=False,
        )


@receiver(post_save, sender=Manager)
def send_manager_details_email(sender, instance, created, **kwargs):
    if created:
        # Compose the email content using the template
        email_subject = 'Here are Your Credentials for Login to Employee Portal : {}'.format(instance.firstName)
        email_body = 'Dear {}\n'.format(instance.firstName)+ f'Manager Name: {instance.firstName}\n' + f'Manager Email: {instance.email}\n'+f'Manager ID : {instance.mID}\n' 
        
        # Send the email
        send_mail(
            email_subject,
            email_body,
            'mansimishra510@gmail.com',  # Sender's email address
            ['mansimishra2314@gmail.com'],  # Recipient's email address
            fail_silently=False,
        )
