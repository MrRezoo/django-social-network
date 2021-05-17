from django import forms

messages = {
    'required': 'این فیلد اجباری است',
    'invalid': 'لطفا یک ایمیل معتبر وارد کنید',

}


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username', 'type': 'username'}))

    password = forms.CharField(max_length=40, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'password', 'type': 'password'}))


class UserRegistrationForm(forms.Form):
    username = forms.CharField(error_messages=messages, max_length=30, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'username', 'type': 'username'}))

    email = forms.EmailField(error_messages=messages, max_length=50, widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'email', 'type': 'email'}))

    password = forms.CharField(error_messages=messages, max_length=40, widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'password', 'type': 'password'}))
