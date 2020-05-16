from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView

from account.decorators import manager_perm_required
from account.forms import UserRegistrationForm, LoginForm, RoomForm, AddStaffToRoomForm
from account.models import Room, CustomUser


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return redirect(reverse('account:login'))
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if user.is_manager():
                        if Room.objects.filter(author=user):
                            return redirect(reverse('account:profile'))
                        else:
                            return redirect(reverse('account:create_room'))
                    else:
                        print(user.username)
                        return redirect(reverse_lazy('account:profile'))
                else:
                    return HttpResponse('аккаунт неактивен')
            else:
                return HttpResponse('Неправильный логин')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@manager_perm_required
@login_required
def create_room(request):
    if request.method == 'POST':
        user = request.user
        form = RoomForm(request.POST)
        if form.is_valid():
            if Room.objects.filter(author=user):
                return HttpResponse('У вас уже есть комната')
            else:
                cd = form.cleaned_data
                title = cd['title']
                staff = cd['staff']
                room = Room.objects.create(title=title, author=request.user)
                staff.update(room=room)
                # redirect room
                return redirect(reverse('account:profile'))
        else:
            return HttpResponse('дурак ты')
    else:
        form = RoomForm()
        return render(request, 'account/room_create.html',
                      {'form': form, })


@login_required
def profile(request):
    user = request.user
    if user.is_manager():
        room = Room.objects.get(author=user)
        staff = room.users.all()
        form = AddStaffToRoomForm()
        return render(request, 'account/manager_profile.html',
                      {'user': user,
                       'room': room,
                       'staff': staff,
                       'form': form})
    else:
        new_room = user.room
        if new_room:
            staff = new_room.users.all()
            return render(request, 'account/room.html',
                          {'user': user,
                           'room': new_room,
                           'staff': staff})
        else:
            return HttpResponse('Вы не состоите ни в одной комнате, обратитесь к менеджеру')


@require_POST
@manager_perm_required
@login_required
def add_staff(request):
    user = request.user
    form = AddStaffToRoomForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        staff = cd['staff']
        room = Room.objects.get(author=user)
        staff.update(room=room)
        return redirect(reverse('account:profile'))
    else:
        return HttpResponse('some error')


class UserDelete(DeleteView):
    model = CustomUser
    success_url = reverse_lazy('account:profile')
    context_object_name = 'usr'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.room = None
        self.object.save()
        return HttpResponseRedirect(success_url)

