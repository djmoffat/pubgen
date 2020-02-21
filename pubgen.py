#!/usr/bin/env python3

# import yaml
# import re
# import sys
# import os

# import biblib
import pdb
from argparse import ArgumentParser
import bibtexparser


def get_args():
    """
    Read the arguments and return them to main.
    """
    parser = ArgumentParser(description="Generate html bibliography from bib file")
    parser.add_argument('-i', '--input', default="publications.bib",
                        help="Input file")
    parser.add_argument('-o', '--output', default="publications.html",
                        help="Output file")
    parser.add_argument('-s', '--sort', default="ENTRYTYPE",
                        help="Which attribute to sort on? ENTRYTYPE, year, name")
    parser.add_argument('-t', '--template', default=None,
                        help="Which template file to use, if any")
    parser.add_argument('-r', '--reference', default=None,
                        help="Which referencing format to use")
    return parser.parse_args()

def open_bib(file):
    with open(file) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    return(bib_database.entries)

def format_authors(names):
    name_list = names.split(' and ')
    if len(name_list) == 1:
        return(name_list[0])
    else:
        return('., '.join(name_list[:-1]) + '. and ' + name_list[-1])

def print_journal(bib):
    author = format_authors(bib['author'])
    print('{} ({}). {}. <i>{}</i>.'.format(author, bib['year'], bib['title'], bib['journal']))

def print_conference(bib):
    author = format_authors(bib['author'])
    print('{} ({}). {}. <i>{}</i>.'.format(author, bib['year'], bib['title'], bib['booktitle']))

def print_patent(bib):
    author = format_authors(bib['author'])
    print('{} ({}). {}. <i>{}</i>.'.format(author, bib['year'], bib['title'], bib['howpublished']))


def format_refs(bib_entries, ref_format):
    if ref_format is None:
        ref_format = 'apa'
    for bib in bib_entries:
        print(bib['ENTRYTYPE'])
        print('<span id="{}">'.format(bib['ID']))
        if bib['ENTRYTYPE'] == 'article':
            print_journal(bib)
        elif bib['ENTRYTYPE'] == 'inproceedings':
            print_conference(bib)
        elif bib['ENTRYTYPE'] == 'bookchapter':
            print_bookchapter(bib)
        elif bib['ENTRYTYPE'] == 'misc':
            print_patent(bib)
        else:
            print(bib['ENTRYTYPE'] + ' : ' + bib['title'])
        print('</span>')


def main(args):
    bib_entries = open_bib(args.input)

    # Sort by month, then year, then by soring requirements
    # bib_database = sorted(bib_entries, key=lambda k: k['month']) 
    bib_entries = sorted(bib_entries, key=lambda k: k['year'], reverse=True) 
    bib_entries = sorted(bib_entries, key=lambda k: k[args.sort]) 
    format_refs(bib_entries, args.reference)

    # print(args)

if __name__ == "__main__":
    args = get_args()
    main(args)
