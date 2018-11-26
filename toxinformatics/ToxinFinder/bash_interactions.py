# Toxinformatics
#
# Created for Biol 469 - Genomics final project
# Fall 2018
#
# Authored by
#     Tyler Marques - tylermarques@gmail.com
#     Michelle Tam
#     Timothy Shardlow
#     Julian Whiting

import subprocess
import os
import argparse
from django.conf import settings
import shutil
import pandas as pd

CRED = '\033[91m'
CEND = '\033[0m'


def save_toxin_hmm_file(organism_name, f):
    with open(f'{settings.BASE_DIR}/results/{organism_name}/Toxins.hmm', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return os.path.abspath(f'"{settings.BASE_DIR}/results/{organism_name}/Toxins.hmm"')


def space_delimited_to_csv(organism_name, hmm_output_path):
    """Runs awk command to clean file and output csv file"""
    print(f'cat "{hmm_output_path}" ' +
          '| awk \'{print $1","$2","$3","$4","$5","$6}\' > ' +
          f'{settings.BASE_DIR}/results/{organism_name}/output.csv')
    subprocess.run(
        f'cat "{hmm_output_path}" ' +
        '| awk \'{print $1","$2","$3","$4","$5","$6}\' > ' +
        f'"{settings.BASE_DIR}/results/{organism_name}/output.csv"',
        shell=True)
    print(CRED + '****Cleaned CSV****' + CEND)


def clean_hmm_output(organism_name, file_path):
    """ The hmm_out file is not only space delimited, it has a bunch of extra crap
    on top and bottom of the file. This function removes the crap so that it can be opened with Pandas."""
    new_file = []
    with open(file_path) as hmm_file:
        lines = hmm_file.readlines()
        lines = lines[1:]
        print(len(lines))
        flag = False
        for line in lines:
            if line[0] == '#' and not flag:
                flag = True
                new_file.append(line[2:])

            elif line[0] == '#' and flag:
                continue
            else:
                new_file.append(line)

    with open(file_path, 'w') as file:
        for line in new_file:
            file.write(f'{line}')
    space_delimited_to_csv(organism_name, file_path)


def show_hmm_out(organism_name):
    """Probably gonna need pandas"""
    hmm_out_file = settings.BASE_DIR + f'/results/{organism_name}/hmm_out.txt'
    clean_hmm_output(organism_name, hmm_out_file)
    df = pd.read_csv(settings.BASE_DIR + f'/results/{organism_name}/output.csv')
    return df.to_html()


def download_genome(genome_link, organism_name):
    subprocess.run([f'wget -O "{settings.BASE_DIR}/results/{organism_name}/{organism_name}.fna" '
                    f'{genome_link}'],
                   shell=True)
    return


def prodigal_proteome_predictions(organism_name, protein_translation):
    results = subprocess.run(
        f'prodigal -i "{settings.BASE_DIR}/results/{organism_name}/{organism_name}.fna" '
        f'-a "{settings.BASE_DIR}/results/{organism_name}/{protein_translation}"',
        shell=True)
    if results.returncode > 0:
        raise ChildProcessError('Something occurred with prodigal, halting forward progress')
    return results.returncode


def prepare_hmm_db(hmm_file_path):
    """Hmm db has to be 'pressed' before it can be used, so this function does that"""
    print(f'hmmpress "{hmm_file_path}"')
    results = subprocess.run([f'hmmpress "{hmm_file_path}"'], shell=True)

    if results.returncode > 0:
        # TODO Add class that deletes previous binaries and remakes them if needed
        # If any of binary files already exist, will raise this error (files named r'.+.hmm.h3*')
        print(results)
        raise ChildProcessError(
            f'Something occured with hmm file prep, halting forward progress. \n Error as follows: {results.returncode}')
    return results


def hmm_per_sequence_hits_table(organism_name, hmm_file_path, protein_translation, file_name):
    if type(file_name) is not str:
        raise ValueError('You were supposed to be a string, dummy.')
    results = subprocess.run(
        f'hmmscan -o "{settings.BASE_DIR}/results/{organism_name}/human_readable.txt" '
        f'--tblout "{settings.BASE_DIR}/results/{organism_name}/{file_name}" '
        f'"{hmm_file_path}" '
        f'"{settings.BASE_DIR}/results/{organism_name}/{protein_translation}"',
        shell=True)
    return results.returncode


def hmm_per_domain_hits_table(toxindb, protein_translation, file_name):
    if type(file_name) is not str:
        raise ValueError('You were supposed to be a string, dummy.')
    results = subprocess.run(
        [f'hmmscan', f'--domtblout {file_name}_domain_hit_table', f'{toxindb}', f'temp/{protein_translation}'])

    return results.returncode


def main(organism_name, genome_link, hmm_file_path):
    if not os.path.exists(f'{settings.BASE_DIR}/results/'):
        # TODO Add this section to setup.py
        os.mkdir(f'{settings.BASE_DIR}/results/')

    if not os.path.exists(f'{settings.BASE_DIR}/results/{organism_name}/'):
        os.mkdir(f'{settings.BASE_DIR}/results/{organism_name}/')

    download_genome(genome_link, organism_name)

    prodigal_proteome_predictions(organism_name, 'protein_translation')

    # TODO check if press is needed before attempting it
    if os.path.exists(f'{settings.BASE_DIR}/results/{organism_name}/hmm_db/'):
        shutil.rmtree(f'{settings.BASE_DIR}/results/{organism_name}/hmm_db/')

    os.mkdir(f'{settings.BASE_DIR}/results/{organism_name}/hmm_db/')
    shutil.copy(hmm_file_path, f'{settings.BASE_DIR}/results/{organism_name}/hmm_db/temp.hmm')
    hmm_file_path = f'{settings.BASE_DIR}/results/{organism_name}/hmm_db/temp.hmm'

    prepare_hmm_db(hmm_file_path)

    # TODO Rename the below argument 'protein_translation' to whatever the file actually is
    hmm_per_sequence_hits_table(organism_name, hmm_file_path, 'protein_translation', 'hmm_out.txt')

    return f'{settings.BASE_DIR}/results/{organism_name}/output.csv'

#
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-l', '--link', help="Your link to the .fna or .faa file")
#     parser.add_argument('-hmm', help='Path to .hmm')
#     args = parser.parse_args()
#
#     main(args.link, args.hmm)
