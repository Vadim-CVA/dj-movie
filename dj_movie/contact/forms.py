from django import forms
from .models import Contact
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV3

class ContactForm(forms.ModelForm):
    """Форма подписки по email"""
    captcha = ReCaptchaField(widget=ReCaptchaV3)

    class Meta:
        model = Contact
        fields = ("email","captcha")
        widget = {
            "email": forms.TextInput(attrs={"class": "editContent", "placeholder": "Your Email ..."})
        }
        labels = {
            "email": ''
        }
