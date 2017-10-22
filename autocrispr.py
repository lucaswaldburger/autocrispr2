
import curses
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
        #
        # if self.genelocus in loci:
        #     loci[self.genelocus] += 1
        #     num = loci[self.genelocus]
        # else:
        #     loci[self.genelocus] = 1
        #     num = loci[self.genelocus]
        # self.name = self.genelocus + '-' + str(num)

    def run(self):
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

        return [self.guides, self.repairs]

def my_raw_input(stdscr, r, c, prompt_string):
    curses.echo()
    stdscr.addstr(r, c, prompt_string)
    stdscr.refresh()
    input = stdscr.getstr(r + 1, c, 20)
    return input  #       ^^^^  reading input at next line

def draw_menu(stdscr):
    k = 0
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        # if k == curses.KEY_DOWN:
        #     cursor_y = cursor_y + 1
        # elif k == curses.KEY_UP:
        #     cursor_y = cursor_y - 1
        # elif k == curses.KEY_RIGHT:
        #     cursor_x = cursor_x + 1
        # elif k == curses.KEY_LEFT:
        #     cursor_x = cursor_x - 1
        #
        # cursor_x = max(0, cursor_x)
        # cursor_x = min(width-1, cursor_x)
        #
        # cursor_y = max(0, cursor_y)
        # cursor_y = min(height-1, cursor_y)

        # Declaration of strings
        title = "Go Go CRISPR!"[:width-1]
        subtitle = "Written by Lucas Waldburger"[:width-1]
        # keystr = "Last key pressed: {}".format(k)[:width-1]
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
        # if k == 0:
        #     keystr = "No key press detected..."[:width-1]

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        # start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - int(height // 2.1))

        # Rendering some text
        # whstr = "Width: {}, Height: {}".format(width, height)
        # stdscr.addstr(0, 0, whstr, curses.color_pair(1))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(1))
        stdscr.attron(curses.A_BOLD)

        # Rendering title
        stdscr.addstr(start_y, start_x_title, title)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(1))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 1, start_x_subtitle, subtitle)
        # stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        # stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        # stdscr.move(cursor_y, cursor_x)



        # #user intials
        # user_init = my_raw_input(stdscr, 5, int(width // 10), "User initials: ").lower()
        # if user_init != "" and len(user_init) > 1 and len(user_init) < 3 :
        #     stdscr.addstr(5,int(width-30) , "User Added!")
        # else:
        #     stdscr.addstr(5,int(width-30), " Invalid input")

        # #current oligo
        # start_oligo = my_raw_input(stdscr, 7, int(width // 10), "Current oligo: ").lower()
        # if user_init != "":
        #     stdscr.addstr(7,int(width-30), "Position Added!")
        # else:
        #     stdscr.addstr(7,int(width-30), " Invalid input")
        #
        # #locus name
        # locus_name = my_raw_input(stdscr, 9, int(width // 10), "Locus name: ").lower()
        # if locus_name != "":
        #     stdscr.addstr(9,int(width-30), "Name Added!")
        # else:
        #     stdscr.addstr(9,int(width-30), " Invalid input")

        #gRNA seq
        grna_in = my_raw_input(stdscr, 5, int(width // 10), "Protospacer: ").lower()
        if grna_in != "" and len(grna_in) == 20:
            stdscr.addstr(5,int(width-30), "Protospacer Added!")
        else:
            stdscr.addstr(5,int(width-30), "Invalid input")

        #genomic seq
        seq_in = my_raw_input(stdscr, 7, int(width // 10), "Genomic sequence (+/- 1 kb): ").lower()
        if seq_in != "" and len(seq_in) > 2000:
            stdscr.addstr(7,int(width-30), "Sequence Added!")
        else:
            stdscr.addstr(7,int(width-30), "Invalid input")

        oligos = Design_CRISPR_Oligos(grna_in,seq_in).run()


        stdscr.addstr(10,int(width // 10),"OUTPUT")
        stdscr.addstr(12, int(width // 10), "forward gRNA \t reverse gRNA \t forward repair DNA \t reverse repair DNA")
        stdscr.addstr(13,int(width//2),oligos[0][0] + "\t" + oligos[0][1] + "\t" + oligos[1][0] + "\t" + oligos[1][1]  )

        # stdscr.addstr(25,30, oligos[0][0] + '\t' + oligos[0][1])

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

def main():
    curses.wrapper(draw_menu)

if __name__ == "__main__":
    main()
