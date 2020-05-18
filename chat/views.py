from django.contrib.auth.mixins import AccessMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, FormView

from account.models import CustomUser
from chat.forms import ChatForm
from chat.models import Chat, Message


class ChatAccessMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        print(kwargs)
        chat = Chat.objects.get(id=kwargs['id'])
        if not request.user.is_authenticated and request.user not in chat.members:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class ChatView(ChatAccessMixin, TemplateView):
    template_name = 'chat/chat.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        chat_id = self.kwargs['id']
        context['chat_id'] = chat_id

        messages = reversed(Message.objects.filter(chat_id=chat_id).order_by('-pub_date')[:15])
        context['messages'] = messages

        chat = Chat.objects.get(id=chat_id)
        context['chat'] = chat

        return context


class ChatListView(ListView):
    template_name = 'chat/index.html'
    model = Chat
    context_object_name = 'chats'

    def get_queryset(self):
        return Chat.objects.filter(members__username=self.request.user.username)


class CreateChatView(FormView):
    template_name = 'chat/create_chat.html'
    form_class = ChatForm
    success_url = reverse_lazy('chat:chat_list')

    def post(self, request, *args, **kwargs):
        chat = ChatForm(request.POST)
        chat.save()

        return HttpResponseRedirect(reverse('chat:chat_list'))


class ChatMembersView(ListView):
    model = CustomUser
    template_name = 'chat/chat_members.html'
    context_object_name = 'members'

    def get_queryset(self):
        chat_id = self.kwargs['id']
        chat = Chat.objects.get(id=chat_id)
        return chat.members.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chat_id = self.kwargs['id']
        context['chat'] = Chat.objects.get(id=chat_id)
        return context

