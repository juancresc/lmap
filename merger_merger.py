import pandas as pd
import operator
import warnings

warnings.filterwarnings("always")


def matches(str1, str2):
    total = 0
    for i in range(len(str1)):
        if str1[i] == str2[i]:
            total += 1
    return total


def merger_merger(input_file_name, output_file_name):
    df = pd.read_csv(input_file_name, sep=",", header=None)
    groups = {}
    for k, v in df.iterrows():
        marker = v[0]
        chr_refseq = v[1]
        pos_refseq = v[2]
        chromosome = v[3]
        position = v[4]
        marker_position = v[5]
        sequence = v[6:]
        sequence = ''.join(sequence.tolist())
        tuple_ = (marker, chromosome, position, sequence, chr_refseq, pos_refseq, marker_position)
        groups.setdefault(str(chromosome) + '_' + str(position), []).append(tuple_)

    result = []
    prev_sequence = False

    for k in sorted(groups.iterkeys()):
        group = groups[k]
        if len(group) == 1:
            marker, chromosome, position, sequence, chr_refseq, pos_refseq, marker_position = group[0]
            str_marker = marker
        else:
            seqs = {}
            markers = []
            for element in group:
                marker, chromosome, position, sequence, chr_refseq, pos_refseq, marker_position = element
                seqs[marker] = sequence
                markers.append(marker)
            values = {}
            for marker, sequence in seqs.iteritems():
                values[marker] = matches(sequence, prev_sequence)
            marker = max(values.iteritems(), key=operator.itemgetter(1))[0]
            sequence = seqs[marker]
            str_marker = ':'.join(markers)
        prev_sequence = sequence
        result.append(
            [str_marker] + [chr_refseq] + [pos_refseq] + list(sequence))

    df = pd.DataFrame(result)
    df.to_csv(output_file_name, sep=",", index=False, header=False)
