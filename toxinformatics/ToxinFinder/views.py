from django.shortcuts import render
from django.http import HttpResponse
from . import bash_interactions as bsh


def index(request):
    return render(request,'index.html')


def run_bash(request):
    if request.method == 'POST':
        hmm_ouput_link = bsh.main(request.POST.get('genome_link', None), request.POST.get('hmm_file', None))
        return HttpResponse(hmm_ouput_link)

