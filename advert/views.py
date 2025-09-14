from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Advertisement
from .forms import AdvertisementForm

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
