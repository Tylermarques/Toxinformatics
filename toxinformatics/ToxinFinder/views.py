from django.shortcuts import render
from django.http import HttpResponse
from . import bash_interactions as bash

CRED = '\033[91m'
CEND = '\033[0m'


def index(request):
    return render(request, 'search.html')


def run_bash(request):
    if request.method == 'POST':
        organism_name = request.POST.get('genome_link', None).split('/')[-2].strip()
        toxin_file_path = request.POST.get('toxin_file_path', None)
        genome_link = request.POST.get('genome_link', None)

        hmm_ouput_link = bash.main(organism_name, genome_link, toxin_file_path)
        table = bash.show_hmm_out(organism_name)

        return render(request, 'results.html', context={'table': table, 'organism_name': organism_name})






