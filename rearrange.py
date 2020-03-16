#!/usr/bin/env python
# encoding: utf-8

from bs4 import BeautifulSoup
import os

WORDPRESSFILE = './untitled2.html'
BLOCK_IDENTIFIER = 'wp:jetpack/layout-grid -->'


def read_txt(wordpressfile):
    """
    Reads a text files line-by-line into a list
    :param wordpressfile: a text file
    :return: a list containing the textfile as a list of lines
    """
    textlines = []

    with open (wordpressfile, 'r') as f:
        for line in f:
            textlines.append(line)
    f.close()


    return textlines


def chunk_text(textlines, block_identifier):

    block_no = 1
    bdict = {}
    bdict[block_no] = []
    i = 0

    while i < len(textlines):
        current_line = textlines[i]

        if block_identifier in current_line:
            block_no+=1
            bdict[block_no] = []
        else:
            bdict[block_no].append(current_line)
        i+=1



    return bdict


def name_chunks(bdict):

    orgdict = {}

    for key in bdict:
        for item in bdict[key]:
            html = BeautifulSoup(item, 'lxml')
            try:
                organisation = html.find('strong').text
                orgdict[organisation] = key
            except:
                pass

    return orgdict

def move_chunks(bdict,orgdict, wordpressfile, block_identifier):

    def write_to_file(payload):
        f = open(newfile, 'a')
        f.write(payload)
        print('hello')
        f.close()
        return


    # Create filename
    newfile = os.path.splitext(wordpressfile)[0] + '_new' + os.path.splitext(wordpressfile)[1]

    other_block_order = []
    org_block_order = []

    # Set up a list of the organisations on the page
    orglist = list(orgdict.keys())
    orglist.sort()

    # Get an alphabetical list of the organisation related blocks
    for current_org in orglist:
        org_block_order.append(orgdict[current_org])

    # Work out which blocks are not organisation related and save them
    for i in range (1, len(bdict)):
        if i not in org_block_order:
            other_block_order.append(i)

    #Calculate longest list
    if len(org_block_order) > len(other_block_order):
        longest_list = len(org_block_order)
    else:
        longest_list = len(other_block_order)

    print(org_block_order)
    print(other_block_order)


    # The 0 is to account for zero indexing
    for j in range(0, longest_list):
        #print(j)
        #print()
        try:
            other_no = other_block_order[j]
            #print(bdict[other_no])
            print('also hello')
            write_to_file(bdict[other_no])
            #print(block_identifier)
            write_to_file(block_identifier)
        except:
            pass

        try:
            org_no = org_block_order[j]
            #print(bdict[org_no])
            write_to_file(bdict[org_no])
            #print(block_identifier)
            write_to_file(block_identifier)
        except:
            pass






    return

def main():
    """
    Main function to run program
    """
    textlines = read_txt(WORDPRESSFILE)

    bdict = chunk_text(textlines, BLOCK_IDENTIFIER)

    orgdict = name_chunks(bdict)

    #move_chunks(bdict, orgdict, WORDPRESSFILE, BLOCK_IDENTIFIER)

if __name__ == '__main__':
    main()