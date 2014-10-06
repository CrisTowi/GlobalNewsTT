#encoding:utf-8
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

from Principal.models import Subseccion

from models import Usuario
User = get_user_model()

PRIVACIDAD_CHOISE = [('publico','Publico'),
         ('privado','Privado')]

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


class NuevaNotaForm(forms.Form):

    titulo      = forms.CharField(label='Titulo', widget=forms.TextInput(attrs={'placeholder': 'Titulo', 'class':'form-control'}))
    descripcion = forms.CharField(label='Descripcion',widget=forms.Textarea(attrs={'placeholder': 'Descripcion', 'class':'form-control'}))
    imagen      = forms.ImageField(label='Imagen', required=False)
    subseccion  = forms.ModelChoiceField(label='Subseccion', queryset=Subseccion.objects.all(), empty_label="(Vacio)")
    privacidad  = forms.ChoiceField(choices=PRIVACIDAD_CHOISE, widget=forms.RadioSelect())

class NuevoUsuarioForm(forms.Form):

    username    = forms.CharField(label='Username', widget=forms.TextInput(attrs={'placeholder': 'Username', 'class':'form-control'}))
    nombre      = forms.CharField(label='Nombre',widget=forms.TextInput(attrs={'placeholder': 'Name', 'class':'form-control'}))
    ap_paterno  = forms.CharField(label='Apellido Paterno',widget=forms.TextInput(attrs={'placeholder': 'Apellido Paterno', 'class':'form-control'}))
    ap_materno  = forms.CharField(label='Apellido Materno',widget=forms.TextInput(attrs={'placeholder': 'Apellido Materno', 'class':'form-control'}))
    email       = forms.EmailField(label='Email', required=False, widget=forms.TextInput(attrs={'placeholder': 'Email', 'class':'form-control'}))
    bio         = forms.CharField(label='Bio',widget=forms.Textarea(attrs={'placeholder': 'Bio', 'class':'form-control'}))

    password1   = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class':'form-control'}))
    password2   = forms.CharField(label='Password (De nuevo)',widget=forms.PasswordInput(attrs={'placeholder': 'Password (De nuevo)', 'class':'form-control'}))

    imagen      = forms.ImageField(label='Imagen', required=False)

    def clean_password2(self):
        cd = self.cleaned_data
        password1 = cd.get('password1')
        password2 = cd.get('password2')
        if password2 != password1:
            raise forms.ValidationError('Los dos passwords deben ser iguales')
        return password2


class LoginForm(forms.Form):

    username  = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Username', 'class':'form-control'}))
    password  = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class':'form-control'}))


