#!/usr/bin/env python

# Standard library imports

import sys
import os
import getopt

# Related Library imports
from enum import Enum
from mako.template import Template
from mako.runtime import Context
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from shutil import copyfile


class ErrorCodes(Enum):
    ARGS_ERROR = 1
    SYSCMD_ERROR = 2
    OK = 0



def parse_args():
    '''
    Parse command-line arguments
    :returns [str]: list of options read
    '''
    inputfile = ''
    outdir_asn = ''
    outdir_support = ''
    try:
        args = sys.argv[1:]
        optlist, args = getopt.gnu_getopt(
            args,
            'hn:',
            ['help', "lib-name="])
        print(optlist)
    except:
        usage()
        sys.exit(ErrorCodes.ARGS_ERROR.value)

    for opt, arg in optlist:
        if opt == '-h':
            usage()
            sys.exit(ErrorCodes.OK.value)
        elif opt in ('-n', '--lib-name'):
            lib_name = arg

    options = [lib_name]

    return options

def usage():
    '''
    Print command-line usage
    '''
    print('Usage: generateASN -i <inputfile> -o1 <outdir-asn> -o2 <outdir-support>  ')

def write_templates(template_names,lib_name,prefix,outdir):
    for t in template_names:
        name_file = os.path.join(outdir, t.rstrip('.mako'))
        if not os.path.isfile(name_file):
            template = Template(filename=prefix+t)
            buf = StringIO()
            ctx = Context(buf, lib_name=lib_name)
            template.render_context(ctx)
            f = open(name_file, 'w')
            f.write(buf.getvalue())
            f.close()


def main():
    options = parse_args()

    lib_name = options[0]

    print(lib_name)

    autoproj_current_root = os.environ.get('AUTOPROJ_CURRENT_ROOT')

    if not autoproj_current_root:
        print("Error, environement variable AUTOPROJ_CURRENT_ROOT does not exist")
        return ErrorCodes.SYSCMD_ERROR.value


    out_asn = os.path.join(autoproj_current_root,'types/',lib_name)

    template_names = ['manifest.xml.mako', 'CMakeLists.txt.mako', 'README.txt.mako']

    if not os.path.exists(out_asn):

        os.makedirs(out_asn)
        prefix = "templates_asn/"
        write_templates(template_names,lib_name,'templates_asn/',out_asn)

    out_asn = os.path.join(out_asn, 'asn')

    template_names = ["CMakeLists.txt.mako"]

    if not os.path.exists(out_asn):
        os.makedirs(out_asn)
        write_templates(template_names,lib_name,'templates_asn/asn/',out_asn)


    out_support = os.path.join(autoproj_current_root,'types/',lib_name + '_support')

    template_names = ['manifest.xml.mako', 'CMakeLists.txt.mako', 'README.md.mako']

    if not os.path.exists(out_support):
        os.makedirs(out_support)
        
    prefix = "templates_support/"
    write_templates(template_names, lib_name, prefix, out_support)

    out_src = os.path.join(out_support, 'src')

    template_names = ["CMakeLists.txt.mako"]

    if not os.path.exists(out_src):
        os.makedirs(out_src)
    write_templates(template_names, lib_name, 'templates_support/src/', out_src)
    copyfile('templates_support/src/lib_name_support.pc.in',os.path.join(out_src,lib_name+'_support.pc.in'))

if __name__ == '__main__':
    main()
