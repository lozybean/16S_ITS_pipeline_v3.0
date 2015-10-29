#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
Created on Oct 20, 2015

@author: root
'''
import os
import sys
from settings import *
def makedirs(dirs):
    for dir in dirs:
        if os.path.isdir(dir):
            return None
        if dir == '':
            return None
        os.system('mkdir -p %s'%dir)



def get_html(cfg_in,vars=None):
    command = []

    reload(sys)
    sys.setdefaultencoding('utf-8')
    work = Work(DEFAULT_CONFIG_DIR + '/get_html_2.cfg')
    work.set_params(cfg_in,vars)
    work.load_default_config()
    config = work.config


    work_dir = config.get('params','work_dir')
    group_files = config.get('params','group_files')
    html_template = config.get('params','html_template')

    outfiles = config.get_section('outfiles')
    scripts = config.get_section('scripts')

    out_dir_report=work_dir+'/'+'report/'
    os.system('rm -Rf %s'%out_dir_report)
    os.makedirs(out_dir_report)
    image_dir = out_dir_report+'/images/'
    dirs = []
    dirs.append(image_dir+"/alpha/")
    dirs.append(image_dir+"/class/")
    dirs.append(image_dir+"/family/")
    dirs.append(image_dir+"/genus/")
    dirs.append(image_dir+"/order/")
    dirs.append(image_dir+"/phylum/")
    dirs.append(image_dir+"/alpha_div_collated/")
    dirs.append(image_dir+"/group/otu_diff/")
    dirs.append(image_dir+"/group/genus_diff/")
    dirs.append(image_dir+"/group/taxall_diff/")
    dirs.append(image_dir+"/group/phylum_diff/")
    makedirs(dirs)
    origin = config.items('origin')

    group_files = re.split('\s+',config.get('params','group_files'))
    group_file_origin =group_files[0]
    group_file = re.search('.+\/(.+)\..+', group_file_origin).group(1)
    #     copy html-demo
    command.append('cp -rf '+html_template+'/* '+out_dir_report+'\n')
    for key,value in origin:
        if(config.has_option('origin', key)):
            match = re.match(r".*png$",value)
            if(match):
                    value_rep = value.replace("#group",group_file)
                    command.append('cp '+work_dir+'../'+value_rep+' '+image_dir+config.get('target',key)+'\n')
            else:
                continue
        else:
            print '06_get_html.cfg no have '+key
    command.append('python %s -c %s \n'%(scripts['get_html'],config.get('outfiles','config')))
    command.append('wkhtmltopdf %s %s \n'%(out_dir_report+'/pdf.html',out_dir_report+'/report.pdf'))
    work.commands.append(''.join(command))

    return outfiles
if __name__ == '__main__':
    config = sys.argv[1]
    get_html(config)

