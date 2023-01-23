from django.shortcuts import render

# Create your views here.


def register_view(request):
    return render(request, 'author/pages/register_view.html')
