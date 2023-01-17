from telegram_django_bot.td_viewset import TelegaViewSet, UserViewSet as TGUserViewSet
from telegram_django_bot.forms import UserForm
from telegram_django_bot.models import BotMenuElem
from telegram_django_bot.utils import handler_decor
from django.conf import settings
from telegram_django_bot.telegram_lib_redefinition import InlineKeyboardButtonDJ
from django.utils.translation import (gettext as _, gettext_lazy)
from telegram_django_bot.routing import telega_reverse
from telegram_django_bot.tg_dj_bot import TG_DJ_Bot
from telegram import Update
from .forms import BotMenuElemForm
from .models import User


@handler_decor()
def start(bot: TG_DJ_Bot, update: Update, user: User):
    message = (
        f'Aloha, {user.first_name or user.telegram_username or user.id}! I am bot, which is made from template 🤖 \n'
        'The goal is to show how it works 😄'
    )  # brackets just for beautiful multi row strings

    buttons = [
        [InlineKeyboardButtonDJ(
            text=_('🧩 BotMenuElem'),
            callback_data=BotMenuElemViewSet(telega_reverse('base:BotMenuElemViewSet')).gm_callback_data('show_list')
        )],
        [InlineKeyboardButtonDJ(text=_('⚙️ Settings'), callback_data='us/se')],
    ]

    # here 2 examples of construct callback_data: just make utrl your self in string or
    # generate it with telega_reverse (construct utrl part to BotMenuElemViewSet) and
    # gm_callback_data (add method and args to Viewset)

    return bot.edit_or_send(update, message, buttons)


class BotMenuElemViewSet(TelegaViewSet):
    viewset_name = 'BotMenuElem'
    telega_form = BotMenuElemForm
    queryset = BotMenuElem.objects.all()

    prechoice_fields_values = {
        'is_visable': (
            (True, '👁 Visable'),
            (False, '🚫 Disabled'),
        )
    }

    def create(self, field=None, value=None):

        if field is None and value is None:
            # then it is starting adding
            self.user.clear_status(commit=False)

        initial_data = {
            'is_visable': True,
            'callbacks_db': '[]',
            'buttons_db': '[]',
        }

        return self.create_or_update_helper(field, value, 'create', initial_data=initial_data)

    def show_list(self, page=0, per_page=10, columns=1):
        __, (mess, buttons) = super().show_list(page, per_page, columns)
        buttons += [
            [InlineKeyboardButtonDJ(
                text=_('➕ Add'),
                callback_data=self.gm_callback_data('create')
            )],
            [InlineKeyboardButtonDJ(
                text=_('🔙 Back'),
                callback_data=settings.TELEGRAM_BOT_MAIN_MENU_CALLBACK
            )],
        ]
        return self.CHAT_ACTION_MESSAGE, (mess, buttons)





class UserViewSet(TGUserViewSet):
    telega_form = UserForm
    use_name_and_id_in_elem_showing = False

    def show_elem(self, model_id=None, mess=''):
        mess = _('⚙️ Settings\n\n')
        __, (mess, buttons) = super().show_elem(self.user.id, mess)
        buttons.append([
            InlineKeyboardButtonDJ(
                text=_('🔙 Main menu'),
                callback_data=settings.TELEGRAM_BOT_MAIN_MENU_CALLBACK
            ),
        ])
        return self.CHAT_ACTION_MESSAGE, (mess, buttons)


@handler_decor()
def some_debug_func(bot: TG_DJ_Bot, update: Update, user: User):
    # the message is written in Django notation for translation (with compiling language you can easy translate text)
    message = _(
        'This func is able only in DEBUG mode. press /some_debug_func'
        'to see this elem. By using handler_decor you have user instance %(user)s and some other features'
    ) % {
        'user': user
    }

    buttons = [[
        InlineKeyboardButtonDJ(
            text=_('🔙 Main menu'),
            callback_data=settings.TELEGRAM_BOT_MAIN_MENU_CALLBACK
        ),
    ]]

    return bot.edit_or_send(update, message, buttons)