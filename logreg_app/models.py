from django.db import models
import re

class RegistrationManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # try:
        #     user = User.objects.get(email = post_data['email'])
        #     errors['email'] = 'Email address is already in use.'
        # except:
        #     pass
        if not email_regex.match(post_data['email']):
            errors['email'] = 'Invalid email address provided'

        if len(User.objects.filter(email = post_data['email']))!= 0:
            errors['email'] = 'Email address is already in use.'

        if len(post_data["first_name"]) < 2:
            errors["error_first_name"] = "Please enter first name of more than 2 characters"
        
        if len(post_data["last_name"]) < 2:
            errors["error_last_name"] = "Please enter last name of more than 2 characters"
        
        if len(post_data["password"]) < 8:
            errors["password_length"] = "The password provided must be 8 characters minimum."

        if post_data['password'] != post_data['confirm_pw']: errors['password_match'] = 'The entered passwords do not match.'
        
        return errors

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.EmailField(320)
    password = models.CharField(max_length = 60)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = RegistrationManager()

class JobManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}

        if len(post_data['job']) < 3:
            errors['job'] = 'Job must be at least 3 characters.'

        if len(post_data['description']) < 3:
            errors['description'] = 'Description must be at least 3 characters.'

        if len(post_data['location']) < 3:
            errors['location'] = 'Location must be at least 3 characters.'

        return errors

class Job(models.Model):
    job = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    location = models.CharField(max_length = 255)
    created_job = models.ForeignKey(User, related_name ='job_created', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = JobManager()

