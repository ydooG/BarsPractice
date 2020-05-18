from django.views.generic import DetailView, CreateView

from vcs.forms import RepositoryCreateForm
from vcs.models import Repository


class RepositoryView(DetailView):
    model = Repository
    template_name = 'vcs/repository.html'
    context_object_name = 'repository'


class CreateRepositoryView(CreateView):
    template_name = 'vcs/create_rep.html'
    model = Repository
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = RepositoryCreateForm()
