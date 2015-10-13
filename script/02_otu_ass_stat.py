#!/usr/bin/env python
from __future__ import division
import sys
import os
import re
import argparse
import numpy as np
from collections import OrderedDict

def read_params(args):
    parser = argparse.ArgumentParser(description='otu assignment statistic | v1.0 at 2015/10/13 by liangzb')
    parser.add_argument('-t','--tax_ass',dest='tax_ass',metavar='FILE',type=str,required=True,
            help="set the tax_assignment file")
    parser.add_argument('-i','--otu_mapfile',dest='otu_map',metavar='FILE',type=str,required=True,
            help="set the otu_mapfile")
    parser.add_argument('-o','--out_file',dest='out_file',metavar='FILE',type=str,required=True,
            help="set the output stat file")

    args = parser.parse_args()
    params = vars(args)
    return params

def read_otu_ass(otu_ass_file):
    ass_num = OrderedDict()
    ass_num['No. of OTUs'] = 0
    tax_level_dict = {'k':'Kingdom','p':'Phylum','c':'Class','o':'Order',
                      'f':'Family','g':'Genus','s':'Species'}
    with open(otu_ass_file) as otu_ass:
        for line in otu_ass:
            tabs = line.strip().split('\t')
            taxes = tabs[1].split(';')
            for tax in taxes:
                short_name = re.search('^(\w)__',tax).group(1)
                keyname = 'Assigned to %s'%tax_level_dict[short_name]
                if keyname not in ass_num:
                    ass_num[keyname] = 0
                ass_num[keyname] += 1
            ass_num['No. of OTUs'] += 1
    return ass_num

def read_otu_mapfile(result,otu_mapfile):
    otu_per_sample = {}
    with open(otu_mapfile) as otu_map:
        for line in otu_map:
            tabs = line.strip().split('\t')
            otu_name = tabs.pop(0)
            otu_sample = set()
            for tab in tabs:
                sample_name = re.search('(.+)_\d+$',tab).group(1)
                if sample_name in otu_sample:
                    continue
                otu_sample.add(sample_name)
                if sample_name not in otu_per_sample:
                    otu_per_sample[sample_name] = 0
                otu_per_sample[sample_name] += 1
    samples = list(otu_per_sample.itervalues())
    samples = np.array(samples)
    result['Min no. of OTUs per sample'] = np.min(samples)
    result['Max no. of OTUs per sample'] = np.max(samples)
    result['Mean no. of OTUs per sample'] = np.mean(samples)
    result['Sd no. of OTUs per sample'] = np.std(samples)
    return result

def write_output(result,outfile):
    with open(outfile,'w') as fp:
        for keyname,value in result.iteritems():
            fp.write('%s\t%s\n'%(keyname,value))

if __name__ == '__main__':
    params = read_params(sys.argv)
    if not os.path.isdir(os.path.dirname(params['out_file'])):
        os.mkdir(os.path.dirname(params['out_dir']))

    result = read_otu_ass(params['tax_ass'])
    result = read_otu_mapfile(result,params['otu_map'])
    result = write_output(result,params['out_file'])

