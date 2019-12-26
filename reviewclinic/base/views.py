from http.client import HTTPResponse

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View
from django_seed import Seed
from django.db.models import Q

from .forms import CommentForm, ReplyForm, ClinicForm
# Create your views here.
from .models import Clinic, Province
from .models import Comment


def index(request):
    keyword = request.GET.get('keyword', None)
    if keyword:
        list_clinic = Clinic.objects.filter(Q(name__contains=keyword) | Q(address__contains=keyword))
    else:
        list_clinic = Clinic.objects.all()
    paginator = Paginator(list_clinic, 10)
    page_number = request.GET.get('page')
    try:
        clinics = paginator.get_page(page_number)
    except PageNotAnInteger:
        clinics = paginator.get_page(1)
    except EmptyPage:
        clinics = paginator.get_page(paginator.num_pages)
    list_comment = Comment.objects.all().order_by('-created_at')[:10]
    context = {'list': clinics, 'listComment': list_comment, 'p': keyword }
    return render(request, 'base/home.html', context)


def view_review(request, clinic_id):
    clinic = Clinic.objects.get(pk=clinic_id)
    list_comment = Comment.objects.filter(clinic_id=clinic_id)
    paginator = Paginator(list_comment, 10)
    page_number = request.GET.get('page')
    try:
        comment = paginator.get_page(page_number)
    except PageNotAnInteger:
        comment = paginator.get_page(1)
    except EmptyPage:
        comment = paginator.get_page(paginator.num_pages)
    f = CommentForm(initial={'rate': '3'})
    reply = ReplyForm()
    return render(request, 'base/detail.html',
                  {'clinic': clinic, 'listComment': comment, 'form': f, 'reply_form': reply})


def save_comment(request):
    if request.method == 'POST':
        c = CommentForm(request.POST)
        if c.is_valid():
            c.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        else:
            return HTTPResponse().status('400')
    return render(request, 'base/footer.html')


def save_reply(request):
    if request.method == 'POST':
        reply = ReplyForm(request.POST)
        if reply.is_valid():
            reply.save()
            next = request.POST.get('next', '/')
            return HttpResponseRedirect(next)
        else:
            return render(request, 'base/review-modal.html')
    return render(request, 'base/footer.html')


class ClassClinic(View):
    def get(self, request):
        clinic_form = ClinicForm()
        list_clinic = Clinic.objects.all()

        return render(request, "base/add-clinic.html", {'list': list_clinic, 'form': clinic_form})

    def post(self, request):
        c = ClinicForm(request.POST)
        clinic_form = ClinicForm()
        list_clinic = Clinic.objects.all()
        er = 1
        if c.is_valid():
            c.save()
            return render(request, "base/add-clinic.html",
                          {'list': list_clinic, 'form': clinic_form, 'error': c.validate_unique()})
        return render(request, "base/add-clinic.html", {'list': list_clinic, 'form': clinic_form, 'error': er})
