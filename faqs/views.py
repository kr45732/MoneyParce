from django.shortcuts import render

# Create your views here.
def index(request):
    template_data = {}
    template_data['title'] = 'Freqently Asked Questions'


    faqs = [
        {
            "question": "What is MoneyParce?",
            "answer": (
                "MoneyParce is a simple web app that helps you set monthly budgets, "
                "track your income and expenses by category, and see where your "
                "money is going."
            ),
        },
        {
            "question": "How do I create an account?",
            "answer": (
                "Click “Sign Up” in the top-right, enter your email, username, "
                "and a password, then confirm via the link we email you."
            ),
        },
        {
            "question": "How do I set or change my budget?",
            "answer": (
                "Once you’re logged in, go to Budget → Edit, pick your spending "
                "limit and (optionally) a default category, then hit Save."
            ),
        },
        {
            "question": "How do I add an expense or income?",
            "answer": (
                "Under Transactions, choose Add Expense or Add Income, fill in "
                "the amount, date, category and a short description, then click Submit."
            ),
        },
        {
            "question": "Can I view a report of my spending?",
            "answer": (
                "Yes—go to Overview to see charts and tables breaking down your "
                "expenses by category and date range."
            ),
        },
    ]

    return render(request, 'faqs/index.html', {
        'template_data': template_data,
        'faqs': faqs,
        })