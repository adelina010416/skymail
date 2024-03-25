from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from user_message.forms import MessageForm
from user_message.models import Message


# Create your views here.
class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('message:all_messages')

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


class MessageDetailView(DetailView):
    model = Message

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


class MessageListView(ListView):
    model = Message


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm

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
        return reverse('message:message', args=[self.kwargs.get('pk')])


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy('message:all_messages')
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
