# H2020 ESROCOS Project
# Company: GMV Aerospace & Defence S.A.U.
# Licence: GPLv2

import sys
import os
import shutil

from mako.template import Template
from mako.runtime import Context

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from . import ErrorCodes

def write_package_templates(templates, libname, templ_dir, outdir):
    '''
    Write a set of Mako templates for a package.
    '''
    for t in templates:
        outfname = os.path.join(outdir, t.rstrip('.mako'))
        if not os.path.isfile(outfname):
            template = Template(filename=os.path.join(templ_dir, t))
            buf = StringIO()
            ctx = Context(buf, lib_name=libname)
            template.render_context(ctx)
            f = open(outfname, 'w')
            f.write(buf.getvalue())
            f.close()
        else:
            print('File {} exists. Skipped.'.format(outfname))


def create_asn1_package_structure(lib_name, out_dir):
    '''
    Create the packages for the ASN.1 types (if exists, doesn't overwrite).
    '''
    
    print('Creating the structure for the types package {}.'.format(lib_name))

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not os.path.exists(os.path.join(out_dir, 'asn')):
        os.makedirs(os.path.join(out_dir, 'asn'))
        
    templ_dir = os.path.join(os.path.dirname(__file__), 'templates', 'types_package')
    templates = ['manifest.xml.mako', 'CMakeLists.txt.mako', 'README.txt.mako', os.path.join('asn', 'CMakeLists.txt.mako')]

    write_package_templates(templates, lib_name, templ_dir, out_dir)
    


def create_support_package_structure(lib_name, out_dir):
    '''
    Create the packages for the conversion functions.
    '''
    
    print('Creating the structure for the support package {}_support.'.format(lib_name))

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    if not os.path.exists(os.path.join(out_dir, 'src')):
        os.makedirs(os.path.join(out_dir, 'src'))

    templ_dir = os.path.join(os.path.dirname(__file__), 'templates', 'support_package')
    templates = ['manifest.xml.mako', 'CMakeLists.txt.mako', 'README.md.mako', os.path.join('src', 'CMakeLists.txt.mako')]

    write_package_templates(templates, lib_name, templ_dir, out_dir)

    # .pc.in file
    pc_in = os.path.join(templ_dir, 'src', 'lib_name_support.pc.in')
    shutil.copyfile(pc_in, os.path.join(out_dir, 'src', '{}_support.pc.in'.format(lib_name)))

