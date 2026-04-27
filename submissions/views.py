from django.shortcuts import render

from django.shortcuts import render, redirect
from .forms import MovieSubmissionForm
from django.contrib.auth.decorators import login_required


@login_required
def submit_movie(request):
    if request.method == 'POST':
        form = MovieSubmissionForm(request.POST)
        if form.is_valid():
            sub = form.save(commit=False)
            sub.user = request.user
            sub.save()
            return redirect('search')
    else:
        form = MovieSubmissionForm()

    return render(request, 'submissions/form.html', {'form': form})