from django.contrib.auth.mixins import *
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import *

from account.models import Room
from bp_manager.models import Team, Board, Process


class TeamCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('account:login')
    model = Team
    fields = ['name', 'managers', 'workers', 'board']
    template_name = 'bp_manager/create_form.html'

    def test_func(self):
        return self.request.user.is_manager()


class BoardCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('account:login')
    model = Board
    fields = ['name', 'room']
    template_name = 'bp_manager/create_form.html'

    def test_func(self):
        return self.request.user.is_manager()


class ProcessCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('account:login')
    model = Process
    fields = ['name', 'board', 'status']
    template_name = 'bp_manager/create_form.html'

    def test_func(self):
        return self.request.user.is_manager()


class TeamUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('account:login')
    model = Team
    fields = ['name', 'managers', 'workers', 'board']
    template_name = 'bp_manager/update_form.html'

    def test_func(self):
        return self.request.user.is_manager()


class BoardUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('account:login')
    model = Board
    fields = ['name', 'room']
    template_name = 'bp_manager/update_form.html'

    def test_func(self):
        return self.request.user.is_manager()


class ProcessUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('account:login')
    model = Process
    fields = ['name', 'board', 'status']
    template_name = 'bp_manager/update_form.html'

    def test_func(self):
        return self.request.user.is_manager()


class TeamDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = reverse_lazy('account:login')
    model = Team
    template_name = 'bp_manager/update_form.html'

    def test_func(self):
        return self.request.user.is_manager()


class BoardDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = reverse_lazy('account:login')
    model = Board
    template_name = 'bp_manager/update_form.html'

    def test_func(self):
        return self.request.user.is_manager()


class ProcessDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = reverse_lazy('account:login')
    model = Process
    template_name = 'bp_manager/update_form.html'

    def test_func(self):
        print(self.request.user)
        return self.request.user.is_manager()


class TeamCreateByBoardView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('account:login')
    model = Team
    fields = ['name', 'managers', 'workers']
    template_name = 'bp_manager/create_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.board = get_object_or_404(Room, pk=self.kwargs['id'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        return self.request.user.is_manager()


class BoardCreateByRoomView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('account:login')
    model = Board
    fields = ['name']
    template_name = 'bp_manager/create_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.room = get_object_or_404(Room, pk=self.kwargs['id'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        return self.request.user.is_manager()


class ProcessCreateByBoardView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('account:login')
    model = Process
    fields = ['name', 'status']
    template_name = 'bp_manager/create_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.board = get_object_or_404(Room, pk=self.kwargs['id'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        return self.request.user.is_manager()


class BoardDetail(LoginRequiredMixin, DetailView):
    model = Board
    template_name = 'bp_manager/board_detail_manager.html'
    login_url = reverse_lazy('account:login')

    def get(self, request, *args, **kwargs):
        if self.request.user.room is None:
            return redirect(reverse_lazy('account:profile'))
        elif not self.request.user.is_manager():
            self.template_name = 'bp_manager/board_detail_stuff.html'
        return super().get(request, *args, **kwargs)