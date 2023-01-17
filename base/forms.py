from telegram_django_bot.models import BotMenuElem
from django.utils.translation import gettext_lazy as _
from django import forms
from telegram_django_bot import forms as td_forms
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, Bot, error
from django.conf import settings
import json
from django.utils import timezone


class BotMenuElemForm(td_forms.TelegaModelForm):
    form_name = _("Menu elem")

    class Meta:
        model = BotMenuElem
        fields = ['command', "is_visable", "callbacks_db", "message", "buttons_db"]
        # labels = {
        #     "text": _("Text"),
        #     "media_id": _('Media'),
        # }
        # widget = {
        #     "entities": forms.HiddenInput(),
        #     "author": forms.HiddenInput(),
        # }

    def clean(self):

        # data = self.data
        cleaned_data = super().clean()

        self.cleaned_data = cleaned_data
        return self.cleaned_data

