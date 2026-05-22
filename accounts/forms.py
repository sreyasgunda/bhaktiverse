from django import forms
from .models import CustomUser

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        }),
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        }),
        label='Confirm Password'
    )
    residency = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. Gandipet'
        }),
        label='Residency Name'
    )

    class Meta:
        model = CustomUser
        fields = ['name', 'phone_number', 'email', 'interesting_skills', 'role']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. +1234567890'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e.g. devotee@bhaktiverse.org'}),
            'interesting_skills': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'e.g. Kirtan instruments, Cooking, Deity Worship, IT support...'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match!")
        
        return cleaned_data

    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password'),
            name=self.cleaned_data.get('name'),
            phone_number=self.cleaned_data.get('phone_number'),
            interesting_skills=self.cleaned_data.get('interesting_skills'),
            role=self.cleaned_data.get('role', 'Devotee')
        )
        if hasattr(user, 'profile'):
            user.profile.residency = self.cleaned_data.get('residency')
            user.profile.save()
        return user


