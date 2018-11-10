# Toxinformatics
#
# Created for Biol 469 - Genomics final project
# Fall 2018
#
# Authored by
#     Tyler Marques - tylermarques@gmail.com
#     Michelle Tam
#     Timothy Shardlow
#     Julian Whitting

import subprocess
import os
import argparse


def download_genome(genome_link, organism_name):
    subprocess.run(['wget', f'-O{organism_name}.fna', f'{genome_link}'])
    return


def prodigal_proteome_predictions(file_name, protein_translation):
    # The output from here will be .faa
    # print(['prodigal',f'-i {file_name}'])
    if not os.path.exists(file_name):
        file_name = file_name.split('.')[0] + '/' + file_name
    results = subprocess.run(f'prodigal -i {file_name} -a {protein_translation}', shell=True)
    if results.returncode > 0:
        raise ChildProcessError('Something occured with prodigal, halting forward progress')
    return results.returncode


def hmm_per_sequence_hits_table(toxindb, protein_translation, file_name):
    if type(file_name) is not str:
        raise ValueError('You were supposed to be a string, dummy.')
    # print(f'hmmscan',f'--tblout {file_name}_sequence_hit_table {toxindb} {protein_translation}')
    results = subprocess.run(
        [f'hmmscan -o human_readable.txt --tblout {file_name} {toxindb} {protein_translation}'],
        shell=True)
    return results.returncode


def hmm_per_domain_hits_table(toxindb, protein_translation, file_name):
    if type(file_name) is not str:
        raise ValueError('You were supposed to be a string, dummy.')
    results = subprocess.run(
        [f'hmmscan', f'--domtblout {file_name}_domain_hit_table', f'{toxindb}', f'temp/{protein_translation}'])

    return results.returncode


def main(genome_link, hmm):
    organism_name = genome_link.split('/')[-2].strip()
    os.chdir('ToxinFinder')
    if not os.path.exists(f'{organism_name}/'):
        os.mkdir(f'{organism_name}/')
    os.chdir(f'{organism_name}/')

    # print(organism_name)
    # print(os.getcwd())

    download_genome(genome_link, organism_name)

    # print(f'Analyzing {organism_name} for Toxins')
    # print('prodical result code', prodigal_proteome_predictions(organism_name + '.fna', 'protein'))

    # TODO Rename the below argument 'protein_translation' to whatever the file actually is
    hmm_per_sequence_hits_table(hmm, 'protein_translation', organism_name + 'hmm_out')
    return os.path.curdir + organism_name + 'hmm_out'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--link', help="Your link to the .fna file")
    parser.add_argument('-hmm', help='Path to .hmm')
    args = parser.parse_args()
    # print(args.link)

    main(args.link, args.hmm)
