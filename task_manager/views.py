from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from account.models import CustomUser
from task_manager.models import *


class TaskCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('account:login')
    model = Task
    fields = ['name', 'description', 'executor', 'role', 'process', 'deadline']
    template_name = 'task_manager/create_form.html'

    def test_func(self):
        return self.request.user.is_manager()

    def form_valid(self, form):
        if self.object.executor is None:
            self.object.status = Task.OPEN
        else:
            if self.object.executor.position != self.object.role:
                return self.render_to_response(self.get_context_data(form=form))
            else:
                self.object.status = Task.IN_PROGRESS
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = reverse_lazy('account:login')
    model = Task
    fields = ['name', 'board', 'status']
    template_name = 'task_manager/update_form.html'

    def test_func(self):
        return self.request.user.is_manager()

    def form_valid(self, form):
        if self.object.executor is None or self.object.executor.position != self.object.role:
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = reverse_lazy('account:login')
    model = Task
    template_name = 'task_manager/update_form.html'

    def test_func(self):
        return self.request.user.is_manager()


class TaskCreateByProcessView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    login_url = reverse_lazy('account:login')
    model = Task
    fields = ['name', 'description', 'executor', 'role', 'deadline']
    template_name = 'task_manager/create_form.html'

    def test_func(self):
        return self.request.user.is_manager()

    def form_valid(self, form):
        if self.object.executor is None:
            self.object.status = Task.OPEN
        else:
            if self.object.executor.position != self.object.role:
                return self.render_to_response(self.get_context_data(form=form))
            else:
                self.object.status = Task.IN_PROGRESS
        self.object = form.save(commit=False)
        self.object.process = get_object_or_404(Room, pk=self.kwargs['id'])
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class StartTask(LoginRequiredMixin, UserPassesTestMixin, RedirectView):
    login_url = reverse_lazy('account:login')
    pattern_name = reverse_lazy('account:profile')

    def test_func(self):
        return not self.request.user.is_manager()

    def get_redirect_url(self, *args, **kwargs):
        task = get_object_or_404(Task, pk=self.kwargs['id'])
        if task.executor is None:
            task.executor = self.request.user
            task.status = Task.IN_PROGRESS
            task.save()
        else:
            pattern_name = reverse_lazy('task_manager:board_view')
        return super().get_redirect_url(*args, **kwargs)


@login_required
def task_list(request, username):
    if username == 'me':
        cur_user = request.user
    else:
        cur_user = get_object_or_404(CustomUser, username=username)
    tasks = Task.objects.filter(executor=cur_user, status=Task.IN_PROGRESS)
    return render(request, 'task_manager/task_list.html',
                  {'usr': cur_user,
                   'tasks': tasks, })
