from django import forms
from .models import AdvUser

class ChangeUserInfoForm(forms.ModelForm):
	email = forms.EmailField(required=True, label='Адрес электронной почты')

	class Meta:
		model = AdvUser
		fields = ('username', 'email', 'first_name', 'last_name', 'send_messages')







from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from .apps import user_registered

class RegisterUserForm(forms.ModelForm):
	email = forms.EmailField(required=True, label='Адрес электронной почты')
	password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, help_text=password_validation.password_validators_help_text_html())
	password2 = forms.CharField(label='Пароль (повторно)', widget=forms.PasswordInput, help_text='Введите тот же самый пароль ещё раз для проверки')

	def clean_password1(self):
		password1 = self.cleaned_data['password1']
		if password1:
			password_validation.validate_password(password1)
		return password1

	def clean(self):
		super().clean()
		password1 = self.cleaned_data['password1']
		password2 = self.cleaned_data['password2']
		if password1 and password2 and password1 != password2:
			errors = {
				'password2': ValidationError('Введённые пароли не совпадают', code='password_mismatch')
			}
			raise ValidationError(errors)

	def save(self, commit=True):
		user = super().save(commit=False)
		user.set_password(self.cleaned_data['password1'])
		user.is_active = False
		user.is_activated = False
		if commit:
			user.save()
		user_registered.send(RegisterUserForm, instance=user)
		return user

	class Meta:
		model = AdvUser
		fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'send_messages')











#форма для подрубрик
from .models import SuperRubric, SubRubric

class SubRubricForm(forms.ModelForm):
	super_rubric = forms.ModelChoiceField(queryset=SuperRubric.objects.all(), empty_label=None, label='Надрубрика', required=True)

	class Meta:
		model = SubRubric
		fields = '__all__'





#форма поиска объявления по введённому слову
class SearchForm(forms.Form):
	keyword = forms.CharField(required=False, max_length=20, label='')






#форма для ввода объявления пользователем
from django.forms import inlineformset_factory
from .models import Bb, AdditionalImage

class BbForm(forms.ModelForm):
	class Meta:
		model = Bb
		fields = '__all__'
		widgets = {'author': forms.HiddenInput}

#набор форм для добавления доп. иллюстраций
AIFormSet = inlineformset_factory(Bb, AdditionalImage, fields='__all__')









from captcha.fields import CaptchaField
from .models import Comment
#форма для комментариев для зарегистрированных пользователей
class UserCommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		exclude = ('is_active',)
		widgets = {'bb': forms.HiddenInput}
#форма для комментариев для гостей
class GuestCommentForm(forms.ModelForm):
	captcha = CaptchaField(label='Введите текст с картинки', error_messages={'invalid': 'Непправильный текст'})

	class Meta:
		model = Comment
		exclude = ('is_active',)
		widgets = {'bb': forms.HiddenInput}
