import argparse

#Takes an amino acid sequence and displays it, formatted with numbers that
#makes more sense when you are creating constructs or mutants

parser = argparse.ArgumentParser()
parser.add_argument('-i', help='Input sequence in plain text format')
parser.add_argument('--start', help='[Optional] Starting position of the sequence')
args=parser.parse_args()

def getStartPosition():
    #Check whether the input is a number
    if ((args.start != None) and (args.start.isdigit() == False)):
        raise ValueError('Start position must be an integer')

    if args.start == None:
        seq_start = 1
    else:
        seq_start = args.start
    return int(seq_start)

def loadProteinSequence():
    sequence_file = args.i
    with open(sequence_file) as f:
        for line in f:
            #If it detects a FASTA format, read the next line instead
            if line.startswith('>'):
                return f.readline()
            else:
                return(line)

def createRuler(seq_length):
    #Define parameters for printing
    formatting_char = '-'
    major_tick_char = '|'
    major_tick_interval = 10 
    ruler = ''
    formatter_counter = 0
    while (formatter_counter < seq_length):
        major_tick_counter = 1 
        while (major_tick_counter < major_tick_interval):
            ruler += formatting_char
            major_tick_counter += 1
            formatter_counter += 1
        if (major_tick_counter == major_tick_interval):
            ruler += major_tick_char
            formatter_counter += 1
    return ruler

def printOutput(sequence, line_width, numbering='on'):
    #This specifies the padding for printing amino acid numbers on the side. Default is
    #set to two.
    number_width = 2
    if (len(sequence) > 9999):
        number_width = 5
    elif (len(sequence) > 999):
        number_width = 4
    elif (len(sequence) > 99):
        number_width = 3
    
    #To get the amino acid string to display properly, a spacer of spaces needs to be
    #added to the beginning before printing. This can't be done with padding as it 
    #results in strange behaviour.
    spacer = ' ' * number_width

    seq_len = len(sequence)
    ruler = createRuler(seq_len)

    #char_pos is the position of the current character being printed. This keeps track
    #of where we are in the string
    char_pos = 0
    while(char_pos < seq_len):
        if (numbering.lower() == 'on'):
            amino_acid_nr = char_pos + getStartPosition()
            #It needs the -1 to remove off-by-one error
            end_amino_acid_nr = char_pos + line_width + getStartPosition() - 1

            #This creates the string to print the ruler for the individual lines.
            sub_ruler = ruler[char_pos:char_pos+line_width]

            #This line prints the amino acid numbers on either end, plus the ruler created
            #with createRuler()
            print('{:>{number_width}} {:} {:<{number_width}}'.format(amino_acid_nr, sub_ruler, end_amino_acid_nr, number_width=number_width))

            #This line prints the amino acid sequence.
            print('{:} {:}'.format(spacer, sequence[char_pos:char_pos+line_width]))

            #Increment the position of the character tracker
            char_pos = char_pos + line_width

            #Add a newline for nicer presentation
            print('\n', end='')

        if (numbering.lower() == 'off'):
            print('{:}'.format(ruler[char_pos:char_pos+line_width])) 
            print('{:}'.format(sequence[char_pos:char_pos+line_width]))
            char_pos = char_pos + line_width

def main():
    printOutput(loadProteinSequence(), 40, numbering='on')

if __name__ == '__main__': main()
