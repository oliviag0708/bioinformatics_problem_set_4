from utility.util import fasta_file_to_dict
from pprint import pprint


def bwt(s):
    """Apply Burrows-Wheeler transform to input string."""
    assert "\002" not in s and "\003" not in s, "Input string cannot contain STX and ETX characters"
    s = "\002" + s + "\003"  # Add start and end of text marker
    table = sorted(s[i:] + s[:i] for i in range(len(s)))  # Table of rotations of string
    last_column = [row[-1:] for row in table]  # Last characters of each row
    return "".join(last_column)  # Convert list of characters into string

def ibwt(r):
    """Apply inverse Burrows-Wheeler transform."""
    table = [""] * len(r)  # Make empty table
    for i in range(len(r)):
        table = sorted(r[i] + table[i] for i in range(len(r)))  # Add a column of r
    s = [row for row in table if row.endswith("\003")][0]  # Find the correct row (ending in ETX)
    return s.rstrip("\003").strip("\002")  # Get rid of start and end markers

if __name__ == '__main__':
	r = bwt('banana')
	print r

	s = ibwt(r)
	print s

	chromosomes = fasta_file_to_dict('data/my_genome.fa')
	#pprint(chromosomes)
	#print chromosomes.keys()
	for key in chromosomes:
		output = open(key + '.fm', 'w')
		print key
		chromosome = chromosomes[key]
		#pprint(chromosome)
		tagged_chromosome = chromosome[0] + '$'
		fm_index = bwt(tagged_chromosome)
		output.write(fm_index)
		output.close()

