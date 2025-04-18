from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Income and Expenses'
    return render(request, 'income_and_expenses/index.html', {
        'template_data': template_data})