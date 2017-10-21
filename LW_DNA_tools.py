
# coding: utf-8

# In[ ]:

def reverse_complement(seq):    
    alt_map = {'ins':'0'}
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'} 
    
    for k,v in alt_map.iteritems():
        seq = seq.replace(k,v)
    bases = list(seq) 
    bases = reversed([complement.get(base,base) for base in bases])
    bases = ''.join(bases)
    for k,v in alt_map.iteritems():
        bases = bases.replace(v,k)
    return bases
def oligo_counter(start,total_entries):
    oligos = []
    oligo_str = start[0:2]
    oligo_num = int(start[2:4])

    while len(oligos) < (total_entries * 4):
        oligos.append(oligo_str+"%02d" % (oligo_num,))
        # same oligo string ==> add 1 to current number
        if oligo_num < 81:
            oligo_num += 1
        # end of oligo string (second letter) ==> start subsequent oligo string (new second letter)
        elif oligo_num == 81 and oligo_str[1] != 'Z':
            oligo_num = 1
            oligo_str = oligo_str[0] + chr(ord(oligo_str[1]) + 1)
        # end of oligo string (second letter) ==> start subsequent oligo string
        else:
            oligo_num = 1
            oligo_str = chr(ord(oligo_str[0]) + 1) + 'A'
    return oligos
