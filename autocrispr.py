import sys
import os
import time
from LW_DNA_tools import *

'''
File name:          autocrispr.py
Author:             Lucas M. Waldburger
Date created:       07/28/17
Date last modified: 10/20/17
Python version:     2.7
Description:        User input is used to generate CRISPR oligos for assembly with pCas9 entry vectors designed by
                    Kevin Schmitz. Output is in the form of a text file that can easily be copy and pasted
                    into the Dueber Lab Website.
'''
# global loci
# loci = {}

class Design_CRISPR_Oligos:

    def __init__(self, protospacer, genomicseq):
        # self.genelocus = genelocus
        self.protospacer = protospacer
        self.genomicseq = genomicseq
        # if self.genelocus in loci:
        #     loci[self.genelocus] += 1
        #     num = loci[self.genelocus]
        # else:
        #     loci[self.genelocus] = 1
        #     num = loci[self.genelocus]
        # self.name = self.genelocus + '-' + str(num)

    def run(self):
        # 5' --> 3' forward gRNA oligo sequence
        fwd_gRNA = 'GACTTT' + self.protospacer

        # 5' --> 3' reverse gRNA oligo sequence
        rev_gRNA = 'AAAC' + reverse_complement(self.protospacer) + 'AA'

        # 5' --> 3' forward repair DNA oligo sequence
        fwd_repairDNA = self.genomicseq[950:950 + 50] + self.genomicseq[
                                                       len(self.genomicseq) - 1000:len(self.genomicseq) - 1000 + 8]
        # 3' --> 5' reverse repair DNA oligo sequence
        rev_repairDNA = self.genomicseq[1000 - 8:1000] + self.genomicseq[
                                                         len(self.genomicseq) - 1000:len(self.genomicseq) - 1000 + 50]

        return [fwd_gRNA,rev_gRNA,fwd_repairDNA,reverse_complement(rev_repairDNA)]
def spinning_cursor():
    while True:
        for cursor in '|/-\\':
            yield cursor
def main():
    print("GO GO CRISPR!")
    protospacer_in = ""
    sequence_in = ""
    while(protospacer_in == "" or sequence_in == ""):
        protospacer_in = raw_input("Protospacer Sequence: ")
        if protospacer_in == "" or len(protospacer_in) != 20:
            print("Invalid input")
            protospacer_in = ""
        sequence_in = raw_input("Genomic Sequence (+/- 1kb): ")
        if sequence_in == "" or len(sequence_in) < 2000:
            print("Invalid input")
            sequence_in = ""
            time.sleep(2)
    spinner = spinning_cursor()
    for _ in range(50):
        sys.stdout.write(spinner.next())
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')
    print("OUTPUT")
    print("fwd gRNA \t rev gRNA \t fwd repair DNA \t rev repair DNA")
    oligos = Design_CRISPR_Oligos(protospacer_in,sequence_in).run()
    for i in oligos:
        print(i)
main()
