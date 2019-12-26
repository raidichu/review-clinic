from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime
from tkinter import CASCADE


# Create your models here.


class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False, blank=False)
    name = models.CharField(max_length=255, null=True, blank=True, default='Ẩn danh')
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def get_date(self):
        time = datetime.now()
        if self.created_at.day == time.day:
            if self.created_at.hour == time.hour:
                return str(time.minute - self.created_at.minnute) + " phút trước"
            else:
                return str(time.hour - self.created_at.hour) + "giờ trước"
        else:
            if self.created_at.month == time.month:
                return str(time.day - self.created_at.day) + " ngày trước"
            else:
                if self.created_at.year == time.year:
                    return str(time.month - self.created_at.month) + " tháng trước "
        return self.created_at

    def __str__(self):
        if self.name:
            return self.name
        return 'Ẩn danh'


def print_star(num):
    output = ''
    for i in range(int(num)):
        output += '<span class="fa fa-star checked"></span>'
    if isinstance(num, float) and (int(num) < num) and num != 5:
        output += '<i class="fa fa-star-half-o checked" aria-hidden ="true"></i>'
        num += 1
    for i in range(5 - int(num)):
        output += '<i class="fa fa-star-o checked" aria-hidden="true"></i>'

    return output


class Clinic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False, blank=False)
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(default='Chưa có mô tả')
    address = models.CharField(max_length=255)
    scale = models.CharField(max_length=255, default='1-50')
    type = models.CharField(max_length=255, default='phòng khám')
    rate = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    logo = models.CharField(max_length=255, default='')

    def star(self):
        list_comment = Comment.objects.filter(clinic_id=self.id)
        c = 0
        if len(list_comment) != 0:
            for item in list_comment:
                c += item.rate
            return c / len(list_comment)
        return 3

    def update_rate(self):
        list_comment = Comment.objects.filter(clinic_id=self.id)
        c = 0
        if len(list_comment) != 0:
            for item in list_comment:
                c += item.rate
            self.rate = c / len(list_comment)
        else:
            self.rate = 3
        self.save()

    def __str__(self):
        return self.name

    def printStar(self):
        return print_star(self.rate)

    def number_comment(self):
        return len(Comment.objects.filter(clinic_id=self.id))


class Comment(Review):
    rate = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    clinic = models.ForeignKey(Clinic, on_delete=CASCADE)
    level = models.CharField(max_length=255, null=True, blank=True, default='Ẩn danh')

    def printStar(self):
        return print_star(self.rate)

    def replies(self):
        replies = Reply.objects.filter(comment_id=self.id)
        return replies

    def save(self, *args, **kwargs):
        clinic = Clinic.objects.get(pk=self.clinic_id)
        super(Comment, self).save(*args, **kwargs)
        clinic.update_rate()


class Reply(Review):
    status = models.CharField(max_length=255)
    comment = models.ForeignKey(Comment, on_delete=CASCADE)

    def get_reaction(self):

        if self.status == "1":
            return '<span class="text-success"> <i class="fa fa-thumbs-up text-success" aria-hidden="true"></i> </span>'
        elif self.status == "2":
            return '<span class="text-danger"> <i class="fa fa-thumbs-down text-danger" aria-hidden="true"></i> </span>'
        else:
            return '<span class="text-dark"> <i class="fa fa-trash" aria-hidden="true"></i> </span>'


class Province(models.Model):
    code = models.CharField(null=True, blank=True, max_length=10)
    name = models.CharField(max_length=100, default='Hà Nội', null=False, blank=False)
