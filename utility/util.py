from pprint import pprint

#comp_map = {"T": "A", "A": "T", "G": "C", "C": "G"}
#sample = "AAAACCCGGT"
#answer = "ACCGGGTTTT"

def get_short_string_position(short_string, long_string):
	pos = long_string.find(short_string)
	if pos == -1:
		return None
	else:
		return pos

def fasta_file_to_dict(in_file):
	fasta = {}
	with open(in_file) as file_one:
	    for line in file_one:
		line = line.strip()
		if not line:
		    continue
		if line.startswith(">"):
		    active_sequence_name = line[1:]
		    if active_sequence_name not in fasta:
			fasta[active_sequence_name] = []
		    continue
		sequence = line
		fasta[active_sequence_name].append(sequence)

	return fasta

def sequence_complement(sequence):
	out_sequence = ""
	for base in sequence:
		out_sequence += complement(base)
	return out_sequence
def reverse_complement(sequence):
	return sequence_complement(sequence)[::-1]

def complement(base):
	return comp_map[base]

def parse_file(filename):
    reads = {}
    with open(filename, 'r') as f:
        content = f.readlines()

        # Recreate content without lines that start with @ and +
        content = [line.rstrip() for line in content if not line[0] in '+B']
	
	read_name = ''
	for line in content:
	    if line.startswith('@'):
		read_name = line[1:]
		reads[read_name] = []
		continue
	    else:
		reads[read_name].append(line)

			
        ## Now the lines you want are alternating, so you can make a dict
        ## from key/value pairs of lists content[0::2] and content[1::2]
        #data = dict(zip(content[0::2], content[1::2]))

    #return data
    return reads

def map_reads(fasta, fastq):
	for read_name in fastq.keys():
		for read in fastq[read_name]:
			reverse_read = reverse_complement(read)
			#print read
			for contig in fasta.keys():
				#print contig
				for sequence in fasta[contig]:
					pos = get_short_string_position(read, sequence)
					if pos is not None:
						#print "match!"
						print "{0},{1},{2},{3},{4}".format(
							read_name,
							contig,
							sequence,
							"+",
							pos)
					pos = get_short_string_position(reverse_read, sequence)
					if pos is not None:
						#print "reverse match!"
						print "{0},{1},{2},{3},{4}".format(
							read_name,
							contig,
							sequence,
							"-", 
							pos)
					

if __name__ == "__main__":
	print "test..."
	print sample
	print reverse_complement(sample)
	fasta = fasta_file_to_dict("my_genome.fa")
	#pprint(fasta)
	print get_short_string_position("brown", "the quick brown fox")
	fastq = parse_file("my_reads.fastq") 
	#pprint(fastq)
	map_reads(fasta, fastq) 
