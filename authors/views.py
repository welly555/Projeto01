from django.http import Http404
from django.shortcuts import render

from .forms import RegisterForm

# Create your views here.


def register_view(request):
    form = RegisterForm()
    return render(request, 'author/pages/register_view.html',
                  {
                      'form': form,
                  })


def register_criate(request):
    if not request.POST:
        raise Http404()

    form = RegisterForm(request.POST)

    return render(request, 'author/pages/register_view.html',
                  {
                      'form': form,
                  })
