from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')  # user will now be available