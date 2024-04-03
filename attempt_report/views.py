from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView

from attempt_report.models import Attempt


# Create your views here.
class AttemptListView(LoginRequiredMixin, ListView):
    model = Attempt

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Attempt.objects.filter(user=self.request.user)
        return context


class AttemptDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Attempt
    success_url = reverse_lazy('report:reports')

    def test_func(self):
        is_owner = Attempt.objects.filter(pk=self.kwargs['pk']).last().user == self.request.user
        return is_owner
