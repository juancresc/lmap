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
        cmd_list = ['Rscript', 'rqtl.R']
        p = Popen(cmd_list, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        if err:
            print('Error in RQTL', err)
            exit()
        print 'out', out
        print "Finding duplicated..."
        df_map = pd.read_csv('map.csv', sep=',', comment='#')
        df_map.columns = ['marker', 'LG', 'cM']
        has_duplicated_cm = False
        chrs = {}
        for k, v in df_map.iterrows():
            pos = str(round(v.cM, 2))
            chromosome = v.LG
            if chromosome in chrs and pos in chrs[chromosome]:
                has_duplicated_cm = True
                print "duplicated: ", chromosome, " ", pos
                break
            chrs.setdefault(chromosome, []).append(pos)

        df_merger = pd.read_csv('merged_.csv', sep=',', comment="#", header=None)
        max_col = max(df_merger.columns)
        df_res = pd.merge(df_merger, df_map, left_on=0, right_on='marker')
        df_res.cM = df_res.cM.round(2)
        df_res.drop('marker', axis=1, inplace=True)
        cols = [0, 1, 2, 'LG', 'cM'] + [l for l in range(3, max_col + 1)]
        df_res = df_res[cols]
        df_res.to_csv('merged_2.csv', header=None, sep=",", index=None)
        if has_duplicated_cm:
            print "Duplicated found, restarting..."
            merger_merger.merger_merger('merged_2.csv', 'merged_.csv')
            keep = True
        else:
            print "No duplicated positions"

    df_res.rename({0: 'marker', 1: 'ref_chromosome', 2: 'ref_position'}, axis=1, inplace=True)
    df_res.to_csv('table.csv', sep=',', index=None)

    #order each LG respect to phisical position

    #order all LG respect to phisical position

    #run rqtl again

    #valildate positions