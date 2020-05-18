from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, CreateView

from account.models import Room
from vcs.forms import RepositoryCreateForm
from vcs.models import Repository
from account.decorators import manager_perm_required


class RepositoryView(DetailView):

    model = Repository
    template_name = 'vcs/repository.html'
    context_object_name = 'repository'

    def get_object(self, queryset=None):
        rep_id = self.kwargs['id']
        return Repository.objects.get(id=rep_id)

    def get(self, request, *args, **kwargs):
        rep_id = self.kwargs['id']
        rep = Repository.objects.get(id=rep_id)
        return render(request, self.template_name, {'repository': rep})


@manager_perm_required
def create_rep(request):
    if request.method == 'GET':
        form = RepositoryCreateForm(initial={'room': request.user.room.id})
        return render(request, 'vcs/create_rep.html', {'form': form})

    elif request.method == "POST":
        form = RepositoryCreateForm(request.POST)
        if form.is_valid():
            rep = form.save()
            room_id = form.cleaned_data['room']
            room = Room.objects.get(id=room_id)
            room.repository = rep
            room.save()
            return redirect(reverse('account:room'))
        else:
            return HttpResponse('Введенная информация неверна')

