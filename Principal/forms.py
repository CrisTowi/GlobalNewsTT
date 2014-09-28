#encoding:utf-8
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model



from models import Usuario
User = get_user_model()

class CrearUsuarioForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Verifica contraseña", widget=forms.PasswordInput)
    imagen    = forms.ImageField(label='Imagen', required=False)


    class Meta:
        model = Usuario
        fields = ('username','nombre','foto','ap_paterno','ap_materno','correo','estado','user_permissions','is_superuser')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden")
        return password2

    def save(self, commit=True):
        user = super(CrearUsuarioForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CambiarusuarioForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="<a href='password/'>Cambiar contraseña</a>")
    imagen    = forms.ImageField(label='Imagen', required=False)

    class Meta:
        model = Usuario
        fields = ('username','nombre','foto','ap_paterno','ap_materno','correo','estado' ,'activo', 'administrador', 'user_permissions', 'is_superuser')

    def clean_password(self):
        return self.initial['password']
