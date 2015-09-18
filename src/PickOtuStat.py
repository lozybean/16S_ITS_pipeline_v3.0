from __future__ import division
import re
import numpy as np
from Bio import SeqIO

class Sample(object):
    def __init__(self,name):
        self.otu_num = 0
        self.stats = {}
        self.otus = set()
        self.stats['tags'] = 0
        self.stats['bases'] = 0
        self.stats['q20'] = 0
        self.stats['q30'] = 0
        self.stats['mapped_tags'] = 0
        self.stats['singleton_tags'] = 0
        self.stats['singleton_ratio'] = 0

class Subject(object):
    def __init__(self):
        self.sample_set = {}

    def read_raw_data_stat(self,file):
        fp=open(file)
        head = fp.next()
        for line in fp:
            sample_name,tags,bases,q20,q30, = line.strip().split('\t')
            if sample_name not in self.sample_set:
                sample = Sample(sample_name)
                self.sample_set[sample_name] = sample
            sample = self.sample_set[sample_name] 
            sample.stats['tags'] = int(tags)
            sample.stats['bases'] = int(bases)
            sample.stats['q20'] = int(q20)
            sample.stats['q30'] = int(q30)
        fp.close()

    def read_single_stat(self,file):
        fp=open(file)
        line = fp.next()
        while(line):
            line = fp.next().strip()
        head = fp.next()
        for line in fp:
            sample_name,tags,single_reads,single_ratio = line.strip().split('\t')
            if sample_name not in self.sample_set:
                sample = Sample(sample_name)
                self.sample_set[sample_name] = sample
            sample = self.sample_set[sample_name]
            sample.stats['tags'] = int(tags)
            sample.stats['singleton_tags'] = int(single_reads)
            sample.stats['singleton_ratio'] = single_ratio
        fp.close()

    def get_mapped_tags_from_uc(self,file):
        fp = open(file)
        for line in fp:
            if not line.startswith('H'):
                continue
            tabs = line.strip().split('\t')
            reads = tabs[8]
            otu_name = tabs[9]
            sample_name = re.search('(.+)_\d+$',reads).group(1)
            if sample_name not in self.sample_set:
                sample = Sample(sample_name)
                self.sample_set[sample_name] = sample
            sample = self.sample_set[sample_name]
            sample.stats['mapped_tags'] += 1
            sample.otus.add(otu_name)
        fp.close()

    def get_mapped_tags_from_otutab(self,file):
        fp = open(file)
        for line in fp:
            tabs = line.strip().split('\t')
            otu_name = tabs.pop(0)
            for tab in tabs:
                sample_name = re.search('(.+)_\d+$',tab).group(1)
                if sample_name not in self.sample_set:
                    sample = Sample(sample_name)
                    self.sample_set[sample_name] = sample
                sample = self.sample_set[sample_name]
                sample.stats['mapped_tags'] += 1
                sample.otus.add(otu_name)
        fp.close()

    def write(self,file):
        fp = open(file,'w')
        fp.write('Sample Number: %s\n'%len(self.sample_set))
        sample_list = list(self.sample_set.itervalues())
        sample_list.sort()
        union_otu = sample_list.pop(0).otus
        for s in sample_list:
            union_otu = union_otu.union(s.otus)
        fp.write('Total OTUs: %s\n'%len(union_otu))
        otu_num = []
        for sample in self.sample_set.itervalues():
            otu_num.append(len(sample.otus))
        otu_num = np.array(otu_num)
        fp.write('OTU average: %2.2f\n'%np.mean(otu_num))
        fp.write('OTU std: %2.2f\n'%np.std(otu_num))
        fp.write('\n')
        fp.write('sample_name\ttags\tmapped_tags\tmapped_ratio\tsingleton_tags\tsingleton_ratio\tQ20_ratio\tQ30_ratio\tOTUs\n')
        for sample_name,sample in self.sample_set.iteritems():
            tags = sample.stats['tags']
            mapped_ratio = sample.stats['mapped_tags'] / tags * 100
            Q20_ratio = sample.stats['q20'] / sample.stats['bases'] * 100
            Q30_ratio = sample.stats['q30'] / sample.stats['bases'] * 100
            fp.write('%s\t%s\t%s\t%2.2f%%\t%s\t%s\t%2.2f%%\t%2.2f%%\t%s\n'%(sample_name,tags,sample.stats['mapped_tags'],mapped_ratio,
                                                                                     sample.stats['singleton_tags'],sample.stats['singleton_ratio'],
                                                                                     Q20_ratio,Q30_ratio,len(sample.otus)))
        fp.close()
     

