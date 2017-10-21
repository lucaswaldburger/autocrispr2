import time
import tkMessageBox
from Tkinter import *
from LW_DNA_tools import *

'''
File name:          autocrispr.py
Author:             Lucas M. Waldburger
Date created:       07/28/17
Date last modified: 09/04/17
Python version:     2.7
Description:        User input is used to generate CRISPR oligos for assembly with pCas9 entry vectors designed by
                    Kevin Schmitz. Output is in the form of a text file that can easily be copy and pasted
                    into the Dueber Lab Website.
'''

global loci
loci = {}

class Design_CRISPR_Oligos:

    def __init__(self, genelocus, protospacer, genomicseq):
        self.genelocus = genelocus
        self.protospacer = protospacer
        self.genomicseq = genomicseq

        if self.genelocus in loci:
            loci[self.genelocus] += 1
            num = loci[self.genelocus]
        else:
            loci[self.genelocus] = 1
            num = loci[self.genelocus]
        self.name = self.genelocus + '-' + str(num)

    def assemble(self):
        # 5' --> 3' forward gRNA oligo sequence
        fw_gRNA = 'GACTTT' + self.protospacer

        # 5' --> 3' reverse gRNA oligo sequence
        rev_gRNA = 'AAAC' + reverse_complement(self.protospacer) + 'AA'
        self.guides = [fw_gRNA, rev_gRNA]

        # 5' --> 3' forward repair DNA oligo sequence
        fw_repairDNA = self.genomicseq[950:950 + 50] + self.genomicseq[
                                                       len(self.genomicseq) - 1000:len(self.genomicseq) - 1000 + 8]
        # 3' --> 5' reverse repair DNA oligo sequence
        rev_repairDNA = self.genomicseq[1000 - 8:1000] + self.genomicseq[
                                                         len(self.genomicseq) - 1000:len(self.genomicseq) - 1000 + 50]
        self.repairs = [fw_repairDNA, reverse_complement(rev_repairDNA)]

        return [self.guides, self.repairs, self.name]

class Options(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.count = 2
        self.entries = []

        user_entry = Entry(self)
        startprimer_entry = Entry(self)
        genelocus_entry = Entry(self)
        protospacer_entry = Entry(self)
        genomic_entry = Entry(self)

        self.user = user_entry
        self.startprimer = startprimer_entry

        user_entry.grid(row=1, column=1)
        startprimer_entry.grid(row=3, column=1)
        genelocus_entry.grid(row=1, column=2)
        protospacer_entry.grid(row=1, column=3)
        genomic_entry.grid(row=1, column=4)

        self.entries.append([genelocus_entry, protospacer_entry, genomic_entry])

    def add(self):
        new_genelocus_entry = Entry(self)
        new_protospacer_entry = Entry(self)
        new_genomic_entry = Entry(self)

        new_genelocus_entry.grid(row=self.count, column=2)
        new_protospacer_entry.grid(row=self.count, column=3)
        new_genomic_entry.grid(row=self.count, column=4)
        self.count += 1

        self.entries.append([new_genelocus_entry, new_protospacer_entry, new_genomic_entry])

    def output(self):
        oligos = []
        loci = {}
        current_user = self.user.get()

        for entry in self.entries:
            oligo = Design_CRISPR_Oligos(entry[0].get(), entry[1].get(), entry[2].get()) #gene locus, protospacer, genomic sequence
            oligos.append(oligo.assemble())

        date = time.strftime("%Y%m%d")
        filename = date + "_GoGoCRISPRoutput.txt"
        file = open(filename, "w")

        # overwrite output file
        file.write("")
        myprimers = oligo_counter(str(self.startprimer.get()), len(self.entries))
        j = 0

        for i in range(len(oligos)):
            file.write(
                myprimers[j] + '.' + current_user + '\t' + oligos[i][0][0] + '\t' + oligos[i][2] + ' fw gRNA\n')
            file.write(
                myprimers[j + 1] + '.' + current_user + '\t' + oligos[i][0][1] + '\t' + oligos[i][2] + ' rev gRNA\n')
            file.write(myprimers[j + 2] + '.' + current_user + '\t' + oligos[i][1][0] + '\t' + oligos[i][
                2] + ' fw repair DNA\n')
            file.write(myprimers[j + 3] + '.' + current_user + '\t' + oligos[i][1][1] + '\t' + oligos[i][
                2] + ' rev repair DNA\n')
            j += 4

        tkMessageBox._show("SUCCESS!", "CRISPR oligos have been saved as " + filename)

def main():
    t = Tk()
    frame = Options(t)
    frame.pack()
    t.title("Go Go CRISPR")
    t.minsize(width=600, height=100)

    titles = ["Initials", "Next Oligo", "Genome Locus", "Protospacer Sequence", "Genomic Sequence (+/- 1 kb)"]
    title_coordinates = [[0, 1, 0], [2, 1, 3], [0, 2, 0], [0, 3, 0], [0, 4, 0]]

    for i in range(len(titles)):
        Label(frame, text=titles[i]).grid(row=title_coordinates[i][0], column=title_coordinates[i][1],
                                          pady=title_coordinates[i][2])

    buttons = ["Quit", "+", "GO GO CRISPR!"]
    button_commands = [frame.quit, frame.add, frame.output]
    button_coordinates = [[0, 0], [0, 5], [0, 6]]

    for j in range(len(buttons)):
        Button(frame, text=buttons[j], command=button_commands[j]).grid(row=button_coordinates[j][0],
                                                                        column=button_coordinates[j][1])

    mainloop()

main()