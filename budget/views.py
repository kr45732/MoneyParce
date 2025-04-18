from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Budget'
    return render(request, 'budget/index.html', {
        'template_data': template_data})