from django.shortcuts import render, redirect
from tracker.models import Transaction
from django.contrib import messages
from django.db.models import Sum
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        amount = request.POST.get('amount')
        if not description or not amount:
            messages.error(request, 'Please fill in all fields.')
            return redirect('/')

        Transaction.objects.create(
            description=description, 
            amount=amount,
            created_by=request.user,
        )
        return redirect('/')
    context = {
        'transactions': Transaction.objects.filter(created_by=request.user),
        'balance': Transaction.objects.filter(created_by=request.user).aggregate(balance = Sum('amount'))['balance'] or 0,
        'income' : Transaction.objects.filter(amount__gte=0, created_by=request.user).aggregate(income = Sum('amount'))['income'] or 0,
        'expense' : Transaction.objects.filter(amount__lte=0, created_by=request.user).aggregate(expense = Sum('amount'))['expense'] or 0,
    }

    return render(request, 'index.html', context)

@login_required(login_url='/login/')
def deleteTransaction(request, uuid):
    Transaction.objects.get(uuid = uuid).delete()
    return redirect('/')

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(
            username = username 
        )
        if not user_obj.exists():
            messages.error(request, 'username not found')
            return redirect('/login/')
        user = authenticate(username = username, password = password)
        if not user:
            messages.error(request, 'Invalid password')
            return redirect('/login/')
        login(request, user)
        return redirect('/')
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('/login/')

def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(
            Q(username = username) | Q(email = email)
        )
        if user_obj.exists():
            messages.error(request, 'Username or email already exists.')
            return redirect('/signup/')
        user = User.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = username,
        )
        user.set_password(password)
        user.save()
        messages.success(request, 'Account created successfully.')
        return redirect('/login/')
        
    return render(request, 'singup.html')