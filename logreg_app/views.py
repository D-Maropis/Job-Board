from django.shortcuts import render, redirect
from .models import User, Job, JobManager
from django.contrib import messages
import bcrypt


def index(request):
    return render(request, 'index.html')

def register(request):
    # print(request.POST)
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(first_name= request.POST['first_name'], last_name= request.POST['last_name'], email= request.POST['email'], password= pw_hash)
        # print(new_user.first_name)
        # print(new_user.last_name)
        # print(new_user.email)
        # print(new_user.password)
        messages.error(request, 'You have successfully registered.  Continue to Login.')
    return redirect('/')

def login(request):

    print(request.POST)
    try:
        user = User.objects.get(email = request.POST['email'])
    except:
        messages.error(request, 'Invalid e-mail address.')
        return redirect('/')
    
    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, 'Invalid e-mail address or password.')
        return redirect('/')
    else:
        request.session['user_id'] = user.id
        request.session['first_name'] = user.first_name
        request.session['email'] = user.email
        return redirect('/users/success')


    return redirect('/')

def success(request):
    if not 'user_id' in request.session:
        messages.error(request, 'Please log in.')
        return redirect('/')
    else:
        job = Job.objects.all()
        context = {
            'jobs': job
        }

        return render(request, 'jobs.html', context)

def logout(request):
    del request.session['user_id']
    del request.session['first_name']
    del request.session['email']
    return redirect('/')

def new_job(request):
    
    return render(request, 'add_job.html')

def add_job(request):
    if request.method == "POST":
        # print(request.POST)
        errors = Job.objects.basic_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/users/new_job')
        else:
            user = User.objects.get(id = request.session['user_id'])
            Job.objects.create(job=request.POST['job'], location=request.POST['location'], description=request.POST['description'], created_job = user)
        print(request.POST)
    return redirect('/users/success')

def cancel(request):

    return redirect('/users/success')

def view_job(request, job_id):
    job = Job.objects.get(id = job_id)

    context = {
        'job' : job
    }
    return render(request, 'view_job.html', context)


def remove_job(request, job_id):
    job = Job.objects.get(id=job_id)
    job.delete()
    return redirect('/users/success')


def edit_job(request, job_id):
    job = Job.objects.get(id=job_id)
    context = {
        'job': job
    }
    return render(request, 'edit_job.html', context)

def update(request, job_id):
    if request.method == "POST":
        # print(request.POST)
        errors = Job.objects.basic_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/users/{job_id}/edit_job')
        else:
            job = Job.objects.get(id= job_id)
            job.job = request.POST['job']
            job.location = request.POST['location']
            job.description = request.POST['description']
            job.save()
            print(request.POST)
        return redirect('/users/success')
