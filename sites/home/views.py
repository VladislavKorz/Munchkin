from django.shortcuts import render
from django.http import HttpResponse
 
def HomeViews(request):
    context = {
        "title": "Моя первая страница",
        "content": "Контент",
    }
    return render(request, 'home/home.html', context)