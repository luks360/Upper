from django import forms
from main.models import User

class RegisterUserForm(forms.ModelForm):

    class Meta:
        password = forms.CharField(widget=forms.PasswordInput())
        email = forms.CharField(widget=forms.EmailInput())
        model=User
        fields='__all__'

        widgets = {
            'password': forms.PasswordInput(),
            'email': forms.EmailInput(),
        }

field_username = RegisterUserForm.base_fields['username']
field_username.widget.attrs["class"] = "form-control"
field_username.widget.attrs["placeholder"] = "Seu nome de usuário"

field_email = RegisterUserForm.base_fields['email']
field_email.widget.attrs["class"] = "form-control"
field_email.widget.attrs["placeholder"] = "Seu e-mail"

field_password = RegisterUserForm.base_fields['password']
field_password.widget.attrs["class"] = "form-control"
field_password.widget.attrs["placeholder"] = "Sua senha"