from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.views.generic import TemplateView

from .models import *
from .forms import AdvertisementForm, ResponseForm
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':  # обработка отправку регистрационной формы пользователя и создание
        user = User.objects.create_user(username=request.POST['username'], email=request.POST['email'],
                                        password=request.POST['password'])

        profile = UserProfile(user=user)
        profile.save()

        token = default_token_generator.make_token(user)  # подтверждение электронной почты
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirmation_url = f"http://example.com/confirm_email/?uid={uid}&token={token}"
        message = render_to_string('confirmation_email.html', {'confirmation_url': confirmation_url})
        send_mail('Confirm your email', message, 'mail', [request.POST['email']])

        return render(request, 'confirmation_sent.html')
    else:

        return render(request, 'registration_form.html')


@login_required
def advertisement_detail(request, ad_id):   # детальное отображение единичных объявлений
    advertisement = Advertisement.objects.get(pk=ad_id)
    return render(request, 'advertisement_detail.html', {'advertisement': advertisement})


@login_required
def create_advertisement(request):  # создание объявления
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            advertisement = form.save(commit=False)
            advertisement.user = request.user
            advertisement.save()
            return redirect('advertisement_detail',
                            ad_id=advertisement.id)
    else:
        form = AdvertisementForm()
    return render(request, 'advertisement_form.html', {'form': form})


def edit_advertisement(request, ad_id):  # редактирование объявлений
    advertisement = Advertisement.objects.get(id=ad_id)
    if request.user == advertisement.user:
        if request.method == 'POST':
            form = AdvertisementForm(request.POST, instance=advertisement)
            if form.is_valid():
                form.save()
                return redirect('advertisement_detail', ad_id=ad_id)
        else:
            form = AdvertisementForm(instance=advertisement)
        return render(request, 'advertisement_form.html', {'form': form})
    else:
        return render(request, 'unauthorized_access.html')


def create_response(request, ad_id):  # написать ответ к объявлению
    advertisement = Advertisement.objects.get(id=ad_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.advertisement = advertisement
            response.user = request.user
            response.save()

            send_mail('New response to your advertisement',
                      f'You have received a new response to your advertisement "{advertisement.title}"',
                      'mail', [advertisement.user.email])
            return redirect('advertisement_detail', ad_id=ad_id)
    else:
        form = ResponseForm()
    return render(request, 'response_form.html', {'form': form, 'advertisement': advertisement})


def private_page(request):
    private_responses = PrivateResponse.objects.filter(private_page__user=request.user)
    return render(request, 'private_page.html', {'private_responses': private_responses})


def send_newsletter(request):
    if request.method == 'POST':
        subject = request.POST['subject']
        content = request.POST['content']
        users = User.objects.all()
        newsletter = Newsletter(subject=subject, content=content)
        newsletter.save()
        newsletter.users.set(users)

        for user in users:
            send_mail(subject, content, 'mail', [user.email])
        return render(request, 'newsletter_sent.html')
    else:
        return render(request, 'newsletter_form.html')


class UserView(LoginRequiredMixin, TemplateView):
    template_name = 'user.html'
