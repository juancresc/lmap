import argparse
import pandas as pd
import merger
import merger_merger
from subprocess import Popen, PIPE
from shutil import copyfile

if __name__ == "__main__":
    parser = argparse.ArgumentParser()  # pylint: disable=invalid-name
    parser.add_argument("-i", "--input", help="Input file")
    parser.add_argument("-o", "--output", help="Output file")
    args = parser.parse_args()  # pylint: disable=invalid-name

    keep = True
    print "Merging..."
    merger.merger(args.input, 'merged.csv')
    copyfile("merged.csv", "merged_.csv")
    while keep:
        keep = False
        print "RQTL..."
        df = pd.read_csv('merged_.csv', sep=',', comment="#", header=None)
        df.rename(columns={0: 'Marker'}, inplace=True)
        df['new_chr'] = 1
        df = df.transpose()
        frames = [df.loc[['Marker', 'new_chr']], df[4:-1]]
        df = pd.concat(frames)
        df.rename(index={'Marker': 'id'}, inplace=True)
        df.rename(index={'new_chr': ''}, inplace=True)
        df.to_csv('rqtl.csv', header=None)
        cmd_list = ['Rscript','rqtl.R']
        p = Popen(cmd_list, stdout=PIPE, stderr=PIPE)
        out,err = p.communicate()
        print out, err

        print "Finding duplicated..."
        df_map = pd.read_csv('map.csv', sep=',', comment='#')
        df_map.columns = ['marker', 'chromosome', 'position']
        has_duplicated_cm = False
        chrs = {}
        for k, v in df_map.iterrows():
            pos = str(round(v.position, 2))
            chromosome = v.chromosome
            if chromosome in chrs and pos in chrs[chromosome]:
                has_duplicated_cm = True
            chrs.setdefault(chromosome, []).append(pos)

            print "Duplicated found, restarting..."
            df_merger = pd.read_csv('merged_.csv', sep=',', comment="#", header=None)
            max_col = max(df_merger.columns)
            df_res = pd.merge(df_merger, df_map, left_on=0, right_on='marker')
            df_res.position = df_res.position.round(2)
            df_res.drop('marker', axis=1, inplace=True)
            cols = [0, 1, 2, 3, 'chromosome', 'position'] + [l for l in range(4, max_col + 1)]
            df_res = df_res[cols]
            df_res.to_csv('merged_2.csv', header=None, sep=",", index=None)
            if has_duplicated_cm:
                merger_merger.merger_merger('merged_2.csv', 'merged_.csv')
                keep = True