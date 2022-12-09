from django import forms
from main.models import Profits, User, GroupProfits, Spending, GroupSpending


class RegisterUserForm(forms.ModelForm):

    class Meta:
        password = forms.CharField(widget=forms.PasswordInput())
        email = forms.CharField(widget=forms.EmailInput())
        model = User
        fields = '__all__'

        widgets = {
            'password': forms.PasswordInput(),
            'email': forms.EmailInput(),
        }


class RegisterProfitsForm(forms.ModelForm):
    value = forms.DecimalField(widget=forms.NumberInput(
        attrs={'placeholder': 'Digite o valor...', 'class': 'form-control'}), decimal_places=2, max_digits=10)
    date = forms.DateField(widget=forms.TextInput(attrs={
                           'placeholder': 'Digite uma data...', 'class': 'form-control'}), input_formats=['%m/%d/%Y'])
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Digite o nome...', 'class': 'form-control'}))

    group = forms.ModelChoiceField(queryset=GroupProfits.objects.all())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RegisterProfitsForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['group'].queryset = self.fields['group'].queryset.filter(
                user=user)
            self.fields['group'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Profits
        fields = ['name', 'value', 'group', 'date']


class EditProfitsForm(forms.ModelForm):
    value = forms.DecimalField(widget=forms.NumberInput(
        attrs={'placeholder': 'Digite o valor...', 'class': 'form-control'}), decimal_places=2, max_digits=10)
    date = forms.DateField(widget=forms.TextInput(attrs={
                           'placeholder': 'Digite uma data...', 'class': 'form-control'}), input_formats=['%m/%d/%Y'])
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Digite o nome...', 'class': 'form-control'}))

    group = forms.ModelChoiceField(queryset=GroupProfits.objects.all())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EditProfitsForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['group'].queryset = self.fields['group'].queryset.filter(
                user=user)
            self.fields['group'].widget.attrs['class'] = 'form-control'
            self.fields['group'].widget.attrs['style'] = 'margin-bottom: 20px;'

    class Meta:
        model = Profits
        fields = ['name', 'value', 'group', 'date']


class RegisterGroupProfitsForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Digite o nome do grupo...', 'class': 'form-control'}))

    class Meta:
        model = GroupProfits
        fields = ['name']


class RegisterSpendingForm(forms.ModelForm):
    value = forms.DecimalField(widget=forms.NumberInput(
        attrs={'placeholder': 'Digite o valor...', 'class': 'form-control'}), decimal_places=2, max_digits=10)
    date = forms.DateField(widget=forms.TextInput(attrs={
                           'placeholder': 'Digite uma data...', 'class': 'form-control'}), input_formats=['%m/%d/%Y'])
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Digite o nome...', 'class': 'form-control'}))

    group = forms.ModelChoiceField(queryset=GroupSpending.objects.all())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RegisterSpendingForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['group'].queryset = self.fields['group'].queryset.filter(
                user=user)
            self.fields['group'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Spending
        fields = ['name', 'value', 'group', 'date']


class EditSpendingForm(forms.ModelForm):
    value = forms.DecimalField(widget=forms.NumberInput(
        attrs={'placeholder': 'Digite o valor...', 'class': 'form-control', 'style': 'margin-bottom: 20px;'}), decimal_places=2, max_digits=10)
    date = forms.DateField(widget=forms.TextInput(attrs={
                           'placeholder': 'Digite uma data...', 'class': 'form-control', 'style': 'margin-bottom: 20px;'}), input_formats=['%m/%d/%Y'])
    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Digite o nome...', 'class': 'form-control', 'style': 'margin-bottom: 20px;'}))

    group = forms.ModelChoiceField(queryset=GroupSpending.objects.all())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(EditSpendingForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['group'].queryset = self.fields['group'].queryset.filter(
                user=user)
            self.fields['group'].widget.attrs['class'] = 'form-control'
            self.fields['group'].widget.attrs['style'] = 'margin-bottom: 20px;'

    class Meta:
        model = Spending
        fields = ['name', 'value', 'group', 'date']


class RegisterGroupSpendingForm(forms.ModelForm):

    name = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Digite o nome do grupo...', 'class': 'form-control'}))

    class Meta:
        model = GroupSpending
        fields = ['name']


field_username = RegisterUserForm.base_fields['username']
field_username.widget.attrs["class"] = "form-control"
field_username.widget.attrs["placeholder"] = "Seu nome de usuário"

field_email = RegisterUserForm.base_fields['email']
field_email.widget.attrs["class"] = "form-control"
field_email.widget.attrs["placeholder"] = "Seu e-mail"

field_password = RegisterUserForm.base_fields['password']
field_password.widget.attrs["class"] = "form-control"
field_password.widget.attrs["placeholder"] = "Sua senha"
