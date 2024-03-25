from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from blog.models import Post
from client.models import Client
from config.urls import scheduler
from mailing.forms import MailForm
from mailing.models import Mail
from mailing.services import *
from users.models import User


# Create your views here.
def home(request):
    """home page"""
    context = {'mailing_amount': Mail.objects.count(),
               'active_mailing_amount': Mail.objects.filter(status='started').count(),
               'object_list': Post.objects.order_by('?')[:3],
               'clients_amount': Client.objects.count()}
    return render(request, 'mailing/home.html', context)


def my_mailing(request):
    """Page with own and saved mailings"""
    context = {'object_list': Mail.objects.all()}
    return render(request, 'mailing/my_mailing.html', context)


def start_mailing(request, pk):
    """Запускает рассылку"""
    mail = Mail.objects.filter(id=pk).first()
    mail.status = 'started'
    mail.save()
    clients = User.objects.get(email=request.user.email).clients.all().values('email')
    client_emails = []
    for client in clients:
        [client_emails.append(i) for i in client.values()]
    start_scheduler(mail, client_emails, request.user.verified_password)
    context = {'object_list': Mail.objects.all()}
    return render(request, 'mailing/my_mailing.html', context)


def stop_mailing(request, pk):
    """Завершает рассылку"""
    mail = Mail.objects.filter(id=pk).first()
    mail.status = 'finished'
    mail.save()
    scheduler.remove_job(str(pk)+str(request.user.verified_password))
    # scheduler.remove_job(str(pk))
    context = {'object_list': Mail.objects.all()}
    return render(request, 'mailing/my_mailing.html', context)


class MailCreateView(CreateView):
    """Create new mailing with new message"""
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mail:my_mails')

    # def get_context_data(self, *args, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #
    #     MessageFormset = inlineformset_factory(Message, Mail, form=MailForm, extra=1)
    #
    #     if self.request.method == 'POST':
    #         context_data['formset'] = MessageFormset(self.request.POST, instance=self.object, )
    #     else:
    #         context_data['formset'] = MessageFormset(instance=self.object)
    #     return context_data
    #
    # def form_valid(self, form):
    #     formset = self.get_context_data()['formset']
    #     self.object = form.save()
    #     if formset.is_valid():
    #         formset.instance = self.object
    #         formset.save()
    #     return super().form_valid(form)


class MailDetailView(DetailView):
    """One mailing"""
    model = Mail

    # def get_context_data(self, *args, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['is_owner'] = False
    #     context['is_moderator'] = False
    #     if self.object.owner == self.request.user:
    #         context['is_owner'] = True
    #     if self.request.user.has_perms(['catalog.set_is_published',
    #                                     'catalog.change_description',
    #                                     'catalog.change_category']):
    #         context['is_moderator'] = True
    #     return context


class MailListView(ListView):
    """All mailings"""
    model = Mail


class MailUpdateView(UpdateView):
    """Update mailing and/or its message"""
    model = Mail
    form_class = MailForm

#
#     def test_func(self):
#         is_owner = Product.objects.filter(pk=self.kwargs['pk']).last().owner == self.request.user
#         return is_owner

    # def get_context_data(self, *args, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #
    #     MailFormset = inlineformset_factory(Message, Mail, form=MessageForm, extra=0)
    #
    #     if self.request.method == 'POST':
    #         context_data['formset'] = MailFormset(self.request.POST, instance=self.object.message, )
    #     else:
    #         context_data['formset'] = MailFormset(instance=self.object.message)
    #     return context_data
    #
    # def form_valid(self, form):

    #     formset = self.get_context_data()['formset']
    #     self.object = form.save()
    #     if formset.is_valid():
    #         formset.instance = self.object
    #         formset.save()
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse('mail:mail', args=[self.kwargs.get('pk')])


class MailDeleteView(DeleteView):
    model = Mail
    success_url = reverse_lazy('mail:my_mails')
#
#     def test_func(self):
#         is_owner = Product.objects.filter(pk=self.kwargs['pk']).last().owner == self.request.user
#         return is_owner
#
#
# class ModeratorProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
#     model = Product
#     form_class = ModeratorProductForm
#     template_name = 'catalog/product_form.html'
#
#     def test_func(self):
#         is_moderator = self.request.user.has_perms(['catalog.set_is_published',
#                                                     'catalog.change_description',
#                                                     'catalog.change_category'])
#         return is_moderator
#
#     def get_context_data(self, *args, **kwargs):
#         context_data = super().get_context_data(**kwargs)
#
#         VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
#
#         if self.request.method == 'POST':
#             context_data['formset'] = VersionFormset(self.request.POST, instance=self.object, )
#         else:
#             context_data['formset'] = VersionFormset(instance=self.object)
#         return context_data
#
#     def form_valid(self, form):
#         formset = self.get_context_data()['formset']
#         self.object = form.save()
#         if formset.is_valid():
#             formset.instance = self.object
#             formset.save()
#         return super().form_valid(form)
#
#     def get_success_url(self):
#         return reverse('catalog:product', args=[self.kwargs.get('pk')])
