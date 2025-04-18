from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Freqently Asked Questions'
    return render(request, 'faqs/index.html', {
        'template_data': template_data})