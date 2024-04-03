from apscheduler.jobstores.base import JobLookupError
from django.contrib.auth.decorators import login_required
from django.core import exceptions
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from blog.models import Post
from client.models import Client
from config.urls import scheduler
from mailing.forms import MailForm
from mailing.models import Mail
from mailing.services import *
from user_message.models import Message
from users.models import User


# Create your views here.
def home(request):
    """home page"""
    context = {'mailing_amount': Mail.objects.count(),
               'active_mailing_amount': Mail.objects.filter(status='started').count(),
               'object_list': Post.objects.order_by('?')[:3],
               'clients_amount': Client.objects.count()}
    return render(request, 'mailing/home.html', context)


@login_required
def my_mailing(request):
    """Page with own and saved mailings"""
    context = {'object_list': Mail.objects.filter(owner=request.user.id)}
    return render(request, 'mailing/my_mailing.html', context)


@login_required
def start_mailing(request, pk):
    """Запускает рассылку"""
    if Mail.objects.filter(id=pk).last().owner == request.user:
        mail = Mail.objects.filter(id=pk).first()
        mail.status = 'started'
        mail.save()
        clients = User.objects.get(email=request.user.email).clients.all().values('email')
        client_emails = []
        for client in clients:
            [client_emails.append(i) for i in client.values()]
        start_scheduler(mail, client_emails, request.user, scheduler)
        context = {'status': 'запущена'}
        return render(request, 'mailing/mail_started.html', context)
    else:
        raise exceptions.PermissionDenied


@login_required
def stop_mailing(request, pk):
    """Завершает рассылку"""
    is_owner = Mail.objects.filter(id=pk).last().owner == request.user
    if is_owner or request.user.has_perm('mailing.set_status'):
        mail = Mail.objects.filter(id=pk).first()
        mail.status = 'finished'
        mail.save()
        try:
            if not is_owner:
                scheduler.remove_job(str(pk) + str(Mail.objects.filter(id=pk).last().owner.verified_password))
            else:
                scheduler.remove_job(str(pk) + str(request.user.verified_password))
        except JobLookupError:
            pass
        # scheduler.remove_job(str(pk))
        context = {'status': 'завершена'}
        return render(request, 'mailing/mail_started.html', context)
    else:
        raise exceptions.PermissionDenied


@login_required
def save_mail(request, pk):
    """Позволяет добавить общую рассылку в 'мои рассылки'"""
    mail = Mail.objects.get(id=pk)
    Mail.objects.create(message=mail.message, name=mail.name, start_time=mail.start_time,
                        frequency=mail.frequency, status='created', owner=request.user)
    Message.objects.create(header=mail.message.header, body=mail.message.body, owner=request.user)
    return render(request, 'mailing/mail_saved.html')


class MailCreateView(LoginRequiredMixin, CreateView):
    """Create new mailing with new message"""
    model = Mail
    form_class = MailForm
    success_url = reverse_lazy('mail:my_mails')

    def form_valid(self, form):
        if form.is_valid():
            mail = form.save()
            mail.owner = self.request.user
            mail.save()
        return super().form_valid(form)

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

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object.owner == self.request.user:
            context['is_owner'] = True
        return context


class MailListView(ListView):
    """All mailings"""
    model = Mail

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.has_perm('mailing.view_mail'):
            context['object_list'] = Mail.objects.all()
            context['is_manager'] = True
            return context
        context['object_list'] = Mail.objects.filter(owner=None)
        return context


class MailUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update mailing and/or its message"""
    model = Mail
    form_class = MailForm

    def test_func(self):
        is_owner = Mail.objects.filter(pk=self.kwargs['pk']).last().owner == self.request.user
        return is_owner

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


class MailDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Mail
    success_url = reverse_lazy('mail:my_mails')

    def test_func(self):
        is_owner = Mail.objects.filter(pk=self.kwargs['pk']).last().owner == self.request.user
        return is_owner
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
