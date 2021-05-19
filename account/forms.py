from django import forms

from account.models import Profile

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


class EditProfileForm(forms.ModelForm):
    username = forms.CharField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = Profile
        fields = ('bio', 'age', 'phone')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'style': 'height: 100px'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class PhoneLoginForm(forms.Form):
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def clean_phone(self):
        phone = Profile.objects.filter(phone=self.cleaned_data.get('phone'))
        if not phone.exists():
            raise forms.ValidationError('This phone number does not exists')
        return self.cleaned_data.get('phone')

class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()