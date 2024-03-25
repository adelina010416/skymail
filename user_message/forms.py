from django import forms

from mailing.forms import StyleFormMixin
from user_message.models import Message


class MessageForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Message
        fields = '__all__'
