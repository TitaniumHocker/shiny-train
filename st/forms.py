# -*- coding: utf-8 -*-
from flask_security.forms import SendConfirmationForm
from wtforms import SubmitField

class CustomSendConfirmationForm(SendConfirmationForm):
    submit = SubmitField(label='Отправить инструкции')
