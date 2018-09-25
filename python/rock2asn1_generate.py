#!/usr/bin/env python3

# H2020 ESROCOS Project
# Company: GMV Aerospace & Defence S.A.U.
# Licence: GPLv2

import sys
import getopt
import errno
import os
from rock2asn1 import packageGenerators, asn1Generators


def main():
    # Parse arguments and obtain types package name from .tlb file
    (tlb_file, outdir_asn, outdir_support) = parse_args()
    lib_name = os.path.splitext(os.path.basename(tlb_file))[0]

    # Create autoproj package structures
    packageGenerators.create_asn1_package_structure(lib_name, outdir_asn)
    packageGenerators.create_support_package_structure(lib_name, outdir_support)

    print('Generating ASN1 types and conversion functions')
    # Create the ASN.1 files and the C/C++ conversion functions
    asn1Generators.generateTypesAndFunctions(tlb_file, os.path.join(outdir_asn, 'asn'), os.path.join(outdir_support, 'src'))

def parse_args():
    '''
    Parse command-line arguments
    :returns (tlbfile, outdir): where tlbfile is the input file and outdir is the output directory for the generated ASN.1 files and code
    '''
    try:
        args = sys.argv[1:]
        optlist, args = getopt.gnu_getopt(
            args,
            'h',
            ['help'])
    except:
        usage()
        sys.exit(errno.EINVAL)
    
    for opt, arg in optlist:
        if opt == '-h':
            usage()
            sys.exit(0)

    if len(args) == 3:
        tlbfile = args[0]
        outdir_asn = args[1]
        outdir_support = args[2]
    else:
        usage()
        sys.exit(errno.EINVAL)

    return (tlbfile, outdir_asn, outdir_support)


def usage():
    '''
    Print command-line usage
    '''
    print('Usage: {} <tlb-file> <outdir-asn> <outdir-support>'.format(sys.argv[0]))


if __name__ == "__main__":
    main()
