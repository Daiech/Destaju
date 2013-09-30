#encoding:utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from apps.account.validators import validate_email_unique


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Correo Electrónico", validators=[validate_email_unique], widget=forms.TextInput(attrs={'placeholder': 'Email', "class": "form-control"}))
    username = forms.CharField(
        label="Nombre de usuario",
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de Usuario', "class": "form-control"}),
        help_text="Requerido. 30 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente."
    )

    class Meta:
        model = User
        fields = ("username", "email",)

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["username"]
        if commit:
            user.save()
        return user


class UserForm(forms.ModelForm):
    email = forms.EmailField(label="Correo Electrónico", validators=[validate_email_unique], widget=forms.TextInput(attrs={'placeholder': 'Email', "class": "form-control", 'type': 'email'}))
    # username = forms.CharField(label="Nombre de usuario", widget=forms.TextInput(attrs={'placeholder': 'Username', "class": "form-control"}))
    first_name = forms.CharField(label="Nombre", widget=forms.TextInput(attrs={'placeholder': 'Nombre', "class": "form-control", "autofocus": "true"}))
    last_name = forms.CharField(label="Apellido", widget=forms.TextInput(attrs={'placeholder': 'Apellido', "class": "form-control"}))

    class Meta:
        model = User
        unique = ('email')
        fields = ('first_name', 'last_name', 'email')

    def save(self):
        print self.cleaned_data["email"]
        user = super(UserForm, self).save()
        return user
