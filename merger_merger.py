import csv
import pandas as pd
import argparse
import operator
import warnings
warnings.filterwarnings("always")

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="Input file",  required=True)
parser.add_argument("-o", "--output", help="Output file",  required=True)
args = parser.parse_args()


def matches(str1, str2):
    total = 0
    for i in range(len(str1)):
        if str1[i] == str2[i]:
            total += 1
    return total


df = pd.read_csv(args.input, sep=",", header=None)
groups = {}
for k,v in df.iterrows():
    marker = v[0]
    pos_refseq = v[1]
    marker_position = v[2]
    chromosome = v[3]
    position = v[4]
    sequence = v[5:]
    sequence = ''.join(sequence.tolist())
    tuple_ = (marker, chromosome, position, sequence,pos_refseq, marker_position)
    groups.setdefault(str(chromosome) + '_' + str(position), []).append(tuple_)

result = []
prev_sequence = False
for k, group in groups.iteritems():

    if len(group) == 1:
        marker, chromosome, position, sequence,pos_refseq, marker_position = group[0]
        str_marker = marker
    else:
        seqs = {}
        markers = []
        for element in group:
            marker, chromosome, position, sequence,pos_refseq, marker_position = element
            seqs[marker] = sequence
            markers.append(marker)
        values = {}
        for marker, sequence in seqs.iteritems():
            values[marker] = matches(sequence, prev_sequence)
        marker = max(values.iteritems(), key=operator.itemgetter(1))[0]
        sequence = seqs[marker]
        str_marker = ':'.join(markers)
    print chromosome, position
    prev_sequence = sequence
    result.append([str_marker] + [pos_refseq] + [marker_position] + [chromosome] + [position] + list(sequence))

df = pd.DataFrame(result)
df.to_csv(args.output, sep=",", index=False,header=False)