#!/usr/bin/env python3

# import yaml
# import re
# import sys
# import os

# import biblib
import pdb
from argparse import ArgumentParser
import bibtexparser


type_names = {'article':'Journal', 'incollection':'Book Chapter', 'inproceedings':'Conference','misc':'Patent'}


def get_args():
    """
    Read the arguments and return them to main.
    """
    parser = ArgumentParser(description="Generate markdown bibliography from bib file")
    parser.add_argument('-i', '--input', default="publications.bib",
                        help="Input file")
    parser.add_argument('-o', '--output', default="publications.md",
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

def return_journal(bib, author):
    return '{} ({}). {}. _{}_.'.format(author, bib['year'], bib['title'], bib['journal'])

def return_bookchapter(bib, author):
    return '{} ({}). {}. {} Editor. _In {}_. {}'.format(author, bib['year'], bib['title'], bib['editor'], bib['booktitle'], bib['publisher'])

def return_conference(bib, author):
    return '{} ({}). _{}_. {}.'.format(author, bib['year'], bib['title'], bib['booktitle'])

def return_patent(bib, author):
    return '{} ({}). _{}_. {}.'.format(author, bib['year'], bib['title'], bib['howpublished'])

def add_links(bib):
    # Links to print
    links = ['pdf', 'url', 'doi', 'audio', 'code']
    out_string = ''
    for link in links:
        # if link == 'DOI':
        #     pdb.set_trace()
        if link.lower() in bib:
            out_string += ' [{}]({})'.format(link.upper(),bib[link])
    # print(out_string)
    return out_string

# def add_bibtex(bib):
#     # Reproduce the bibtex
#     out_string = '<vs-button @click="popupActivo=true" color="primary" type="border">bib</vs-button><vs-popup class="holamundo"  title="bibtex file" :active.sync="popupActivo"><p>'
#     out_string += bibtexparser.dump(db)
#     out_string +='</p></vs-popup>'
#     return out_string

def format_refs(bib_entries, ref_format):
    format_refs = ''
    for ref_type in type_names:
        format_refs += '# ' + type_names[ref_type] + '\n\n'
        for bib in bib_entries:
            if bib['ENTRYTYPE'] == ref_type:
                line_string = '' #<span id="{}">'.format(bib['ID'])
                author = format_authors(bib['author'])
                if bib['ENTRYTYPE'] == 'article':
                    line_string = return_journal(bib, author)
                elif bib['ENTRYTYPE'] == 'incollection':
                    line_string = return_bookchapter(bib, author)
                elif bib['ENTRYTYPE'] == 'inproceedings':
                    line_string = return_conference(bib, author)
                elif bib['ENTRYTYPE'] == 'misc':
                    line_string = return_patent(bib, author)
                else:
                    print(bib['ENTRYTYPE'] + ' : ' + bib['title'])
                line_string = line_string.replace('{','').replace('}','')
                line_string = line_string.replace('\\\"o','&ouml;').replace('\\\'e','&eacute;')
                line_string += add_links(bib)
                # line_string += add_bibtex(bib)
                format_refs += line_string +'\n\n'
    return format_refs

def header():
    return '---\nlayout: default\ntitle: Bibliography\n---\n\n'

def main(args):
    bib_entries = open_bib(args.input)

    # Sort by month, then year, then by soring requirements
    # bib_database = sorted(bib_entries, key=lambda k: k['month']) 
    bib_entries = sorted(bib_entries, key=lambda k: k['year'], reverse=True) 
    bib_entries = sorted(bib_entries, key=lambda k: k[args.sort], reverse=True) 
    ref_string = header()
    ref_string += format_refs(bib_entries, args.reference)
    # print(ref_string)
    # pdb.set_trace()
    with open(args.output,'w') as wf:
        wf.write(ref_string)

    # print(args)

if __name__ == "__main__":
    args = get_args()
    main(args)
