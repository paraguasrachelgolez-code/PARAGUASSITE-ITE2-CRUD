from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Users, Genders


def user_list(request):
    search_query = request.GET.get('search', '')
    
    if search_query:
        users_qs = Users.objects.filter(
            Q(full_name__icontains=search_query) | 
            Q(username__icontains=search_query)
        ).order_by('-user_id')
    else:
        users_qs = Users.objects.all().order_by('-user_id')

    paginator = Paginator(users_qs, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user/UsersList.html', {
        'page_obj': page_obj, 
        'search_query': search_query
    })


def add_user(request):
    genders = Genders.objects.all()
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        birth_date = request.POST.get('birth_date')
        address = request.POST.get('address')
        contact_number = request.POST.get('contact_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        gender_id = request.POST.get('gender')
        profile_picture = request.FILES.get('profile_picture') 

        if Users.objects.filter(username=username).exists():
            messages.error(request, f'Username "{username}" is already taken! Please choose another one.')
            return redirect('add_user')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match! Please try again.')
            return redirect('add_user')

        if len(contact_number) != 11 or not contact_number.isdigit() or not contact_number.startswith('09'):
            messages.error(request, 'Contact number must be exactly 11 digits and start with "09" (e.g., 09123456789).')
            return redirect('add_user')

        hashed_password = make_password(password)
        gender_instance = get_object_or_404(Genders, pk=gender_id)

        Users.objects.create(
            full_name=full_name,
            username=username,
            email=email,
            birth_date=birth_date,
            address=address,
            contact_number=contact_number,
            password=hashed_password,
            gender=gender_instance,
            profile_picture=profile_picture
        )
        
        messages.success(request, 'User successfully added!')
        return redirect('user_list')
        
    return render(request, 'user/AddUser.html', {'genders': genders})


def edit_user(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    genders = Genders.objects.all()

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        birth_date = request.POST.get('birth_date')
        address = request.POST.get('address')
        contact_number = request.POST.get('contact_number')
        gender_id = request.POST.get('gender')
        profile_picture = request.FILES.get('profile_picture')
        
        if Users.objects.filter(username=username).exclude(pk=user_id).exists():
            messages.error(request, f'Username "{username}" is already taken by another user!')
            return redirect('edit_user', user_id=user_id)

        if len(contact_number) != 11 or not contact_number.isdigit() or not contact_number.startswith('09'):
            messages.error(request, 'Contact number must be exactly 11 digits and start with "09" (e.g., 09123456789).')
            return redirect('edit_user', user_id=user_id)

        user.full_name = full_name
        user.username = username
        user.email = email
        user.birth_date = birth_date
        user.address = address
        user.contact_number = contact_number
        user.gender = get_object_or_404(Genders, pk=gender_id)

        if profile_picture:
            user.profile_picture = profile_picture

        user.save()
        messages.success(request, 'User updated successfully!')
        return redirect('user_list')

    return render(request, 'user/EditUser.html', {'user': user, 'genders': genders})


def delete_user(request, user_id):
    user = get_object_or_404(Users, pk=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('user_list')
    return render(request, 'user/DeleteUser.html', {'user': user})

def gender_list(request):
    genders = Genders.objects.all()
    return render(request, 'gender/GendersList.html', {'genders': genders})

def add_gender(request):
    if request.method == 'POST':
        gender_name = request.POST.get('gender')
        if gender_name:
            Genders.objects.create(gender=gender_name)
            messages.success(request, 'Gender added successfully!')
            return redirect('gender_list')
    return render(request, 'gender/AddGender.html')

def edit_gender(request, genderId):
    gender_obj = get_object_or_404(Genders, pk=genderId)
    if request.method == 'POST':
        gender_obj.gender = request.POST.get('gender')
        gender_obj.save()
        messages.success(request, 'Gender updated successfully!')
        return redirect('gender_list')
    return render(request, 'gender/EditGender.html', {'gender': gender_obj})

def delete_gender(request, genderId):
    gender_obj = get_object_or_404(Genders, pk=genderId)
    if request.method == 'POST':
        gender_obj.delete()
        messages.success(request, 'Gender deleted successfully!')
        return redirect('gender_list')
    return render(request, 'gender/DeleteGender.html', {'gender': gender_obj})