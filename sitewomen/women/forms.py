from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Husbund, Women


class AddPostForm(forms.ModelForm):

    cat = forms.ModelChoiceField(queryset=Category.objects.all(),
                                 label='Категории',
                                 empty_label='Категория не выбрана',
                                 )
    husbund = forms.ModelChoiceField(queryset=Husbund.objects.all(),
                                     required=False,
                                     label='Супруг',
                                     empty_label='Не замужем',
                                     )

    class Meta:
        model = Women
        fields = [
            'title',
            'slug',
            'content',
            'photo',
            'is_published',
            'cat',
            'husbund',
            'tags'
        ]
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-input'}
            ),
            'content': forms.Textarea(
                attrs={'cols': 50, 'rows': 5}
            )
        }
        labels = {'slug': 'URL'}

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Слишком длинный заголовок.')
        return title


class UploadFileForm(forms.Form):
    file = forms.ImageField(label='Файл')


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='E-mail')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'wors': 10}), label='Сообщение')
    captcha = CaptchaField(label='Введите код')
