from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm

def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            if request.user.is_authenticated:
	            feedback.user = request.user
	            feedback.save()
	            return redirect('profile') 
            else:
            	feedback.save()
            	return redirect('login') # Создайте страницу благодарности или редирект, как вам нужно
    else:
        form = FeedbackForm()

    return render(request, 'feedback/feedback.html', {'form': form})
