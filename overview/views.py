from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'MoneyParce'
    return render(request, 'overview/index.html', {
        'template_data': template_data})