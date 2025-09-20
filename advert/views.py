from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Advertisement, Response
from .forms import AdvertisementForm, ResponseForm

def ad_list(request):
    ads = Advertisement.objects.all()
    return render(request, 'ad_list.html', {'ads': ads})

def ad_detail(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk)
    return render(request, 'ad_detail.html', {'ad': ad})

@login_required
def my_ads(request):
    ads = Advertisement.objects.filter(author=request.user)
    return render(request, 'my_ads.html', {'ads': ads})

@login_required
def ad_create(request):
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            messages.success(request, 'Объявление успешно создано!')
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdvertisementForm()
    return render(request, 'ad_form.html', {'form': form, 'title': 'Создать объявление'})

@login_required
def ad_edit(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk)
    
    if ad.author != request.user:
        messages.error(request, 'Вы не можете редактировать это объявление')
        return redirect('ad_detail', pk=ad.pk)
    
    if request.method == 'POST':
        form = AdvertisementForm(request.POST, instance=ad)
        if form.is_valid():
            form.save()
            messages.success(request, 'Объявление успешно обновлено!')
            return redirect('ad_detail', pk=ad.pk)
    else:
        form = AdvertisementForm(instance=ad)
    
    return render(request, 'ad_form.html', {'form': form, 'title': 'Редактировать объявление'})

@login_required
def ad_delete(request, pk):
    ad = get_object_or_404(Advertisement, pk=pk)
    
    if ad.author != request.user:
        messages.error(request, 'Вы не можете удалить это объявление')
        return redirect('ad_detail', pk=ad.pk)
    
    if request.method == 'POST':
        ad.delete()
        messages.success(request, 'Объявление успешно удалено!')
        return redirect('my_ads')
    
    return render(request, 'ad_confirm_delete.html', {'ad': ad})

@login_required
def create_response(request, pk):
    advertisement = get_object_or_404(Advertisement, pk=pk)
    
    # Нельзя откликаться на своё объявление
    if advertisement.author == request.user:
        messages.error(request, 'Вы не можете откликнуться на своё объявление')
        return redirect('ad_detail', pk=advertisement.pk)
    
    # Проверяем, не откликался ли уже пользователь
    existing_response = Response.objects.filter(
        advertisement=advertisement,
        sender=request.user
    ).first()
    
    if existing_response:
        messages.info(request, 'Вы уже откликнулись на это объявление')
        return redirect('ad_detail', pk=advertisement.pk)
    
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.advertisement = advertisement
            response.sender = request.user
            response.receiver = advertisement.author
            response.save()
            messages.success(request, 'Ваш отклик успешно отправлен!')
            return redirect('ad_detail', pk=advertisement.pk)
    else:
        form = ResponseForm()
    
    return render(request, 'create_response.html', {
        'form': form,
        'advertisement': advertisement
    })

@login_required
def my_responses(request):
    # Отклики на свои объявления
    received_responses = Response.objects.filter(receiver=request.user).select_related(
        'advertisement', 'sender'
    )
    
    # Отклики, которые я отправил
    sent_responses = Response.objects.filter(sender=request.user).select_related(
        'advertisement', 'receiver'
    )
    
    return render(request, 'my_responses.html', {
        'received_responses': received_responses,
        'sent_responses': sent_responses
    })

@login_required
def update_response_status(request, pk, status):
    response = get_object_or_404(Response, pk=pk)
    
    # Проверяем, что пользователь - автор объявления
    if response.receiver != request.user:
        return HttpResponseForbidden("У вас нет прав для этого действия")
    
    if status in ['accepted', 'rejected']:
        response.status = status
        response.save()
        messages.success(request, f'Статус отклика обновлен на "{response.get_status_display()}"')
    
    return redirect('my_responses')
