from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def index_view(request):
    """Main dashboard view."""
    return render(request, 'dashboard/index.html')
