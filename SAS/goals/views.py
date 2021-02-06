from django.shortcuts import render

# Create your views here.
def index(request):
    context_dict = {'boldmessage':'EXAMPLE'}
    return render(request, 'rango/index.html', context=context_dict)
