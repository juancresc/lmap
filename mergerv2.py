#!/usr/bin/env python
# -*- coding: utf-8 -*-
from itertools import *
from operator import itemgetter
from fnmatch import fnmatch
import sys, csv
import time


def group_wc_in_full(d_wc, merge_full):
    res_no_matches = []
    for wc in d_wc:
        matches = 0
        keys = []
        count = 0
        for full in merge_full:
            if match(full[1], wc[1]):
                keys.append(count)
                matches += 1
            count += 1
        if matches == 1:
            for k in keys:
                full = merge_full[k]
                new_key = full[0] + ", (" + wc[0] + ")"
                merge_full[k] = (new_key, full[1])
        if matches > 1:
            for k in keys:
                full = merge_full[k]
                new_key = full[0] + ", (" + wc[0] + ")"
                merge_full[k] = (new_key, full[1])
        if matches == 0:
            res_no_matches.append(wc)
    return merge_full, res_no_matches


def group_no_wc(mergelist):
    reslist = []
    total_keys = []
    for i in range(len(mergelist)):
        isMatch = False
        compared = False
        keys = []
        anyval = None
        keys.append(mergelist[i][0])
        if mergelist[i][0] in total_keys:
            continue
        for j in range(i + 1, len(mergelist)):
            if mergelist[j][0] in total_keys:
                continue
            compared = True
            if mergelist[i][1] == mergelist[j][1]:
                isMatch = True
                keys.append(mergelist[j][0])
                total_keys.append(mergelist[j][0])
                anyval = mergelist[j][1]
        if compared:
            if isMatch:
                str_keys = ", ".join(keys)
                new_item = (str_keys, anyval)
                reslist.append(new_item)
            else:
                reslist.append(mergelist[i])
    return reslist


def match(v1, v2):
    if not "-" in v1 and not "-" in v2:
        return v1 == v2
    v1_reg = v1.replace("-", "?")
    cont = 0
    for s in v2:
        if s == "-":
            v1_reg = v1_reg[:cont] + "?" + v1_reg[cont + 1:]
        cont += 1
    return fnmatch(v2, v1_reg)


def group_nonmatched(nonmatched):
    pivot = nonmatched[0]
    res = []
    res.append(pivot)
    for i in range(1, len(nonmatched)):
        count = 0
        keys = []
        keys.append(nonmatched[i][0])
        for j in range(len(res)):
            try:
                a = res[j]
            except IndexError:
                continue
            if match(nonmatched[i][1], res[j][1]):
                count += 1
                keys.append(str(res[j][0]))
                del (res[j])
        if count == 0:
            res.append(nonmatched[i])
        else:
            new_tuple = (", ".join(keys), nonmatched[i][1])
            res.append(new_tuple)
    for i in range(len(res)):
        res[i] = ("{" + res[i][0] + "}", res[i][1])
    return res


def merger(input_file_name, output_file_name):
    t = time.process_time()
    input_file = open(input_file_name, 'r', encoding='utf8')
    input_file_csv = csv.reader(input_file, delimiter=',')
    input_file_list = list(input_file_csv)
    d = {}
    print('initial',len(input_file_list[1:]))
    for line in input_file_list[1:]:
        str_line = "".join(line[3:len(line)])
        d[line[0]] = str_line
    input_file.close()
    # d_full = list((key, value) for key, value in d.iteritems())
    d_no_wc = list((key, value) for key, value in d.items() if not "-" in value)
    d_wc = list((key, value) for key, value in d.items() if "-" in value)

    # 1- merge_full <= MERGE d_no_wc
    merge_full = group_no_wc(d_no_wc)

    # 2- merge_full_wc <= MERGE d_wc in merge_full
    merge_full_wc, wc_no_match = group_wc_in_full(d_wc, merge_full)

    # 3 merge nonmatched
    if len(wc_no_match) > 0:
        merged_wc_no_match = group_nonmatched(wc_no_match)
    else:
        merged_wc_no_match = []

    final = merged_wc_no_match + merge_full_wc

    idx = 0
    for row in final:
        positions = {}
        ids = row[0]
        ids = ids.replace("(", "").replace(")", "")
        ids = ids.replace("[", "").replace("]", "")
        ids = ids.replace("{", "").replace("}", "")
        ids = ids.replace(" ", "")
        ids = ids.split(',')
        for id in ids:
            id_clean = id.replace(" ", "")
            for line in input_file_list:
                if line[0] == id_clean:
                    positions.setdefault(line[1], []).append((id_clean, line[2]))
        # get most common element in list (dict keys)
        # if position:
        chromosome = max(set(positions.keys()), key=list(positions.keys()).count)

        _id, position = min(positions[chromosome], key=lambda x: x[1])
        final[idx] += (chromosome, position, _id,)
        idx += 1

    output_file = open(output_file_name, 'w')
    for item in final:
        row = list()
        row.append('"' + item[0] + '"')  #  ids
        row.append(item[2])  # chromosome
        row.append(item[3])  # position
        for c in item[1]:
            row.append(c)
        output_file.write(",".join(row) + "\n")

    print('end', len(final))
    elapsed_time = time.process_time() - t
    print(elapsed_time, 'in seconds')
    output_file.close()
