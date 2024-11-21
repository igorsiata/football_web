from django import forms
from .models import *
from decimal import Decimal


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'body', 'image']
        labels = {
            "title": "Title",
            "body":  "News Content",
            "image": "Image"
        }
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title',
                                            'class': "form-control form-control-lg",
                                            'id': "news_form_title"
                                            }),
            'body': forms.Textarea(attrs={'placeholder': 'Write here',
                                          'class': "form-control",
                                          'id': "news_form_body",
                                          'rows': "10"}),
            'image': forms.ClearableFileInput(attrs={'class': "form-control-file",
                                                     'id': 'news_form_image'
                                                     })
        }
