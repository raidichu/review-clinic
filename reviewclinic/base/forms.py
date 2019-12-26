from django import forms
from django.forms import TextInput

from .models import Clinic, Province
from .models import Comment, Reply


class CommentForm(forms.ModelForm):
    class Meta:
        OPTIONS = (
            ('1', '1 Điểm - Max sida nên tránh xa'),
            ('2', '2 Điểm - Hết thuốc chữa đang tính đường chuồn'),
            ('3', '3 điểm - Cũng tàm tạm đê coi sao'),
            ('4', '4 điểm - Cùng ngon nên làm lâu dài'),
            ('5', '5 điểm - Công ty tuyệt vời có đuổi cũng méo muốn đi'),
        )

        model = Comment
        fields = ('name', 'content', 'rate', 'clinic', 'level',)
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Muốn sưng tên thì xưng, không muốn xưng thì thôi',
                       'id': 'inputName'}),
            'level': forms.TextInput(
                attrs={'class': 'form-control ', 'placeholder': 'Bênh nhân/ Y tá/ Điều dưỡng', 'id': 'inputLevel'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Viết gì đó', 'id': 'inputContent', 'rows': 5, 'minlength': 10}),
            'rate': forms.Select(choices=OPTIONS, attrs={'class': 'form-control w-50', }),
        }


class ReplyForm(forms.ModelForm):
    class Meta:
        OPTIONS = (
            ('1', 'Like'),
            ('2', 'Đếch like'),
            ('3', 'Xóa dùm'),
        )
        model = Reply
        fields = ('name', 'content', 'status', 'comment',)
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Muốn sưng tên thì xưng, không muốn xưng thì thôi',
                       'id': 'inputReplyName'}),
            'content': forms.Textarea(
                attrs={'class': 'form-control replyContent', 'placeholder': 'Viết gì đó', 'id': 'inputReplyContent',
                       'rows': 5, 'minlength': 10}),
            'status': forms.Select(choices=OPTIONS, attrs={'class': 'form-control selectStatus w-50'}),
        }


class ClinicForm(forms.ModelForm):
    class Meta:
        OPTIONS_SCALE = (
            ('1-50', '1-50'),
            ('50-100', '50-100'),
            ('100-150', '100-150'),
            ('150-200', '150-200'),
            ('> 200', ' > 200'),
        )

        OPTIONS_RATE = (
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
        )
        model = Clinic
        fields = ('name', 'description', 'address', 'scale', 'type', 'rate')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Tên',
                       'id': 'inputReplyName'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control replyContent', 'placeholder': 'Viết gì đó', 'id': 'inputReplyContent',
                       'rows': 5}),
            'address': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'địa chỉ',
                       'id': 'inputReplyName'}),
            'rate': forms.Select(choices=OPTIONS_RATE, attrs={'class': 'form-control selectStatus w-50'}),
            'scale': forms.Select(choices=OPTIONS_SCALE, attrs={'class': 'form-control selectStatus w-50'}),
            'type': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Loại',
                       'id': 'inputType'}),
        }
