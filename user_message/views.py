from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from user_message.forms import MessageForm
from user_message.models import Message


# Create your views here.
class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:all_messages')

    def form_valid(self, form):
        if form.is_valid():
            message = form.save()
            message.owner = self.request.user
            message.save()
        return super().form_valid(form)


class MessageDetailView(DetailView):
    model = Message


class MessageListView(ListView):
    model = Message

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Message.objects.filter(owner=self.request.user)
        return context


class MessageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Message
    form_class = MessageForm

    def test_func(self):
        is_owner = Message.objects.filter(pk=self.kwargs['pk']).last().owner == self.request.user
        return is_owner

    def get_success_url(self):
        return reverse('message:message', args=[self.kwargs.get('pk')])


class MessageDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('message:all_messages')

    def test_func(self):
        is_owner = Message.objects.filter(pk=self.kwargs['pk']).last().owner == self.request.user
        return is_owner
