from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from client.forms import ClientForm
from client.models import Client
from users.models import User


# Create your views here.
class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('client:my_clients')

    def form_valid(self, form):
        if form.is_valid():
            client = form.save()
            user = self.request.user
            user.clients.add(client)
            client.save()
        return super().form_valid(form)


class ClientDetailView(LoginRequiredMixin, DetailView):
    model = Client


class ClientListView(LoginRequiredMixin, ListView):
    model = Client

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_list"] = User.objects.get(email=self.request.user.email).clients.all()
        return context


class ClientUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Client
    form_class = ClientForm

    def test_func(self):
        client = User.objects.get(pk=self.request.user.id).clients.filter(id=self.kwargs['pk'])
        if client:
            return True
        return False

    def get_success_url(self):
        return reverse('client:client', args=[self.kwargs.get('pk')])


class ClientDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('client:my_clients')

    def test_func(self):
        client = User.objects.get(pk=self.request.user.id).clients.filter(id=self.kwargs['pk'])
        if client:
            return True
        return False
