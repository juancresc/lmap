import argparse
import pandas as pd
import merger
import merger_merger
from subprocess import Popen, PIPE

if __name__ == "__main__":
    parser = argparse.ArgumentParser()  # pylint: disable=invalid-name
    parser.add_argument("-a", "--annotation", help="Annotation file (.gff3 format)")
    args = parser.parse_args()  # pylint: disable=invalid-name

    keep = True
    while keep:
        keep = False

        merger('input.csv','merged.csv')
        df = pd.read_csv('merged.csv', sep=',', comment="#")
        df = df.transpose()
        df.loc['new_chr'] = 1
        frames = [df.loc[['Marker', 'new_chr']], df[5:]]
        df = pd.concat(frames)
        df.rename(index={'Marker': 'id'}, inplace=True)
        df.rename(index={'new_chr': ''}, inplace=True)
        df.to_csv('rqtl.csv', header=None)

        cmd_list = ['Rscript','rqtl.R','rqtl.csv']
        p = Popen(cmd_list, stdout=PIPE, stderr=PIPE)
        out,err = p.communicate()
        print out, err

        df = pd.read_csv('map.csv', sep=',', comment='#')
        has_duplicated_cm = False

        if has_duplicated_cm:
            merger_merger('assda')
            keep = True