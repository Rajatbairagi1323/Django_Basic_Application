from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm , Add_record_form
from .models import Record

def home(request):
    record = Record.objects.all()
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("Username:", username)
        print("Password:", password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")
            return redirect('home')  
        else:
            messages.error(request, "Username and Password are not correct. Please try again!")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':record})

def logout_user(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            print(form)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            form.save()
            print(form)
            user = authenticate(username=username, password=password)
            login(request, user)
            print(user)
            messages.success(request, "You have successfully registered. Welcome!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def customer_record(request,pk):
    if request.user.is_authenticated:
        # look up records
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "You must be login to view the page!")
        return redirect('home')
    
    
    
def delete_record(request,pk):
    if request.user.is_authenticated:
        delete_it=Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "Record Deleted successfull!")
        return redirect('home')
    else:
        messages.success(request, "You must be logged in to do that......")
        return redirect('home')
           
        
def add_record(request):
    form = Add_record_form(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid():
                add_record = form.save()
                messages.success(request,"Record Added.... ")
                return redirect('home')
        return render(request, 'add_record.html',{'form':form})
        
    else:
        messages.success(request,"You Must Be Logged IN.....")
        return redirect('home')
        
def update_record(request,pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk) 
        form = Add_record_form(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,"Record has been updated")
            return redirect('home')
        return render(request, 'update_record.html',{'form':form})
    else:
        messages.success(request,"You Must Be Logged IN.....")
        return redirect('home')
        
    