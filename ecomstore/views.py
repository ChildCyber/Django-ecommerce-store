from django.shortcuts import render


# Create your views here.
def file_not_found_404(request):
    page_title = "Page Not Found"
    return render(request, locals(), status=404)
