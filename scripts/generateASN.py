#!/usr/bin/env python

# Standard library imports

import sys
import os
import getopt

# Related Library imports
from enum import Enum
import xml.etree.ElementTree as ET
from mako.template import Template
from mako.runtime import Context
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
from shutil import copyfile

# Global variables

#basicTypes = {'bool': 'T-Boolean', 'char': 'T-UInt8', 'int': 'T-Int16', 'float': 'T-Float', 'double': 'T-Double',
#               'int8_t': 'T-Int8', 'uint8_t': 'T-UInt8', 'int16_t': 'T-Int16', 'uint16_t': 'T-UInt16',
#               'int32_t': 'T-Int32', 'uint32_t': 'T-UInt32', 'int64_t': 'T-Int64', 'uint64_t': 'T-UInt64',
#               'float32_t': 'T-Float', 'float64_t': 'T-Double', 'std::string': 'T-String', 'string': 'T-String'}

# list obtained by the command gcc -xc++ -E -v - for C++ compiler, gcc -xc -E -v - for C language

includePath = ['/home/esrocos/esrocos_workspace/install/include/', '/usr/include/c++/5/', '/usr/include/x86_64-linux-gnu/c++/5/', '/usr/include/c++/5/backward', '/usr/lib/gcc/x86_64-linux-gnu/5/include/', '/usr/local/include', '/usr/lib/gcc/x86_64-linux-gnu/5/include-fixed/', '/usr/include/x86_64-linux-gnu/', '/usr/include/']

basicTypes = {'Bool': 'T-Boolean', 'Char': 'T-UInt8', 'Int': 'T-Int16', 'Float': 'T-Float', 'Double': 'T-Double',
               'Int8-t': 'T-Int8', 'Uint8-t': 'T-UInt8', 'Int16-t': 'T-Int16', 'Uint16-t': 'T-UInt16',
               'Int32-t': 'T-Int32', 'Uint32-t': 'T-UInt32', 'Int64-t': 'T-Int64', 'Uint64-t': 'T-UInt64',
               'Float32-t': 'T-Float', 'Float64-t': 'T-Double', 'Std-string': 'T-String', 'String': 'T-String'}

invalidKeywords = [
    "active", "adding", "all", "alternative", "and", "any", "as", "atleast", "axioms", "block", "call", "channel", "comment", "connect", "connection", "constant", "constants", "create", "dcl", "decision", "default", "else", "endalternative", "endblock", "endchannel", "endconnection", "enddecision", "endgenerator", "endmacro", "endnewtype", "endoperator", "endpackage", "endprocedure", "endprocess", "endrefinement", "endselect", "endservice", "endstate", "endsubstructure", "endsyntype", "endsystem", "env", "error", "export", "exported", "external", "fi", "finalized", "for", "fpar", "from", "gate", "generator", "if", "import", "imported", "in", "inherits", "input", "interface", "join", "literal", "literals", "macro", "macrodefinition", "macroid", "map", "mod", "nameclass", "newtype", "nextstate", "nodelay", "noequality", "none", "not", "now", "offspring", "operator", "operators", "or", "ordering", "out", "output", "package", "parent", "priority", "procedure", "process", "provided", "redefined", "referenced", "refinement", "rem", "remote", "reset", "return", "returns", "revealed", "reverse", "save", "select", "self", "sender", "service", "set", "signal", "signallist", "signalroute", "signalset", "spelling", "start", "state", "stop", "struct", "substructure", "synonym", "syntype", "system", "task", "then", "this", "timer", "to", "type", "use", "via", "view", "viewed", "virtual", "with", "xor", "end", "i", "j", "auto", "const",
    # From Nicolas Gillet/Astrium for SCADE
    "abstract", "activate", "and", "assume", "automaton", "bool", "case", "char", "clock", "const", "default", "div", "do", "else", "elsif", "emit", "end", "enum", "every", "false", "fby", "final", "flatten", "fold", "foldi", "foldw", "foldwi", "function", "guarantee", "group", "if", "imported", "initial", "int", "is", "last", "let", "make", "map", "mapfold", "mapi", "mapw", "mapwi", "match", "merge", "mod", "node", "not", "numeric", "of", "onreset", "open", "or", "package", "parameter", "pre", "private", "probe", "public", "real", "restart", "resume", "returns", "reverse", "sensor", "sig", "specialize", "state", "synchro", "tel", "then", "times", "transpose", "true", "type", "unless", "until", "var", "when", "where", "with", "xor",
    # From Maxime - ESA GNC Team
    "open", "close", "flag",
    #From Raquel - ESROCOS
    "name", "size"

]


allInfo = dict()

libraries = dict()

userDefsLib = ''
userDefsSource = ''

libName = ''
sourceName = ''


for key in ['T-Boolean', 'T-Int8', 'T-UInt8', 'T-Int32', 'T-UInt32']:
    libraries[key] = 'TASTE-BasicTypes'
for key in ['T-Int16', 'T-UInt16', 'T-Int64', 'T-UInt64', 'T-Float', 'T-Double', 'T-String']:
    libraries[key] = 'TASTE-ExtendedTypes'

aliasTypes = dict()


class ErrorCodes(Enum):
    ARGS_ERROR = 1
    SYSCMD_ERROR = 2
    OK = 0


class AsnFile():
    ''' Struct for defining each ASN file'''

    def __init__(self, name):
        self.name = name
        # self.importLibraries = dict()  # dictionary to manage all imported types
        self.nameTypes = []
        self.strTypes = []
        self.depsTypes = []


class ConfigTypes():

    def __init__(self, name):
        self.asnName = name
        self.maxDim = []
        self.asnParameters = []
        self.asn1SccParameters = []
        self.asnFields = []
        self.asnTypes = []
        self.rootTypes = []
        self.depsTypes = []
        self.cppFields = []
        self.cppTypes = []
        self.cppName = ''
        self.cppInclude = []
        self.tag = ''
        self.value = None
        self.dimFields = []
        self.asn1SccName = 'asn1Scc' + name.replace('-','_')
        self.asn1SccFields = []
        self.isOpaque = []
        self.idxOpaque = []


class OpaqueType():
    def __init__(self,name, cpp_name, marshall, cpp_marshall):
        self.asnName = [name]
        self.cppName = [cpp_name]
        self.asnMarshall = marshall
        self.cppMarshall = cpp_marshall
        self.cppInclude = []
        brief_name = name.replace('-','_')
        brief_name = brief_name.replace('<','_')
        brief_name = brief_name.replace('>','_')
        self.briefName = [brief_name]

    def add_new_name(self, name, cpp_name):
        self.asnName.append(name)
        self.cppName.append(cpp_name)
        brief_name = name.replace('-','_')
        brief_name = brief_name.replace('<','_')
        brief_name = brief_name.replace('>','_')
        self.briefName.append(brief_name)


opaqueTypes = dict()




allTypes = dict() # dictionary of all ASN types created


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
            'hi:o:s:',
            ['help', "ifile=","outdir-asn=","outdir-support"])
        print(optlist)
    except:
        usage()
        sys.exit(ErrorCodes.ARGS_ERROR.value)

    for opt, arg in optlist:
        if opt == '-h':
            usage()
            sys.exit(ErrorCodes.OK.value)
        elif opt in ('-i', '--ifile'):
            inputfile = arg
        elif opt in ('-o', '--outdir-asn'):
            outdir_asn = arg
        elif opt in ('-s', '--outdir-support'):
            outdir_support = arg

    options = [inputfile, outdir_asn, outdir_support]

    return options

def usage():
    '''
    Print command-line usage
    '''
    print('Usage: generateASN -i <inputfile> -o <outdir-asn> -s <outdir-support>  ')


def remove_templates(str_type):
    is_template = True
    while is_template:
        idx = str_type.find('<')
        idx2 = str_type.find('>')
        if idx != -1:
            str_type = str_type[0:idx] + str_type[idx2+1:-1]
        else:
            is_template = False
    return str_type


def find_type_template(str_template):
    str_template = str_template.partition('<')
    str_template_out = str_template[0]
    str_type = str_template[-1]
    if str_type != '':
        str_type = str_type[0:-1]  #Removing the last character
    return [str_template_out, str_type]


def find_array_dim(str_array):
    str_array = str_array.partition('[')
    array_type = str_array[0]
    dim = str_array[-1].partition(']')
    dim = dim[0]
    return [array_type, dim]


def process_type_field(type_field, name_var=''):

    asn1_type = ''
    deps_types = []
    suffix = []
    parameters = []
    parameter = ''
    cpp_field = ''

    is_template = True
    is_opaque = False
    idx_opaque = -1

    while is_template:
        if type_field in basicTypes:
            is_template = False
        elif type_field in aliasTypes:
            type_field_old = type_field
            type_field = aliasTypes[type_field]
            if type_field in opaqueTypes:
                if type_field_old in opaqueTypes[type_field].asnName:
                    idx_opaque = opaqueTypes[type_field].asnName.index(type_field_old)
                    is_opaque = True
        else:
            is_template = False

    [template, str_type] = find_type_template(type_field)
    if str_type == '':
        type_field = template
    elif template == 'Std-vector':

        [max_dim, parameter] = add_parameter_type (name_var)
        asn1_type += "SEQUENCE (SIZE(1.." + max_dim + ")) OF "

        deps_types.append (parameter)
        deps_types.append ('T-UInt32')

        suffix.append(max_dim)
        parameters.append (parameter)



        #asn1_type += 'SEQUENCE (SIZE(1..200)) OF '
        type_field = str_type
    else:
        print('Strange')
        str_type = str_type.strip()
        nums = str_type.split(',')

        for i in nums:
            if i.isdigit():
                if int(i) != 1:
                    asn1_type += 'SEQUENCE(SIZE(1..' + i + ')) OF '
        type_field = template

    is_template = True

    idx_opaque = -1

    while is_template:
        if type_field.strip('/') in basicTypes:
            is_template = False
        elif type_field in aliasTypes:
            type_field_old = type_field
            type_field = aliasTypes[type_field]
            if type_field in opaqueTypes:
                if type_field_old in opaqueTypes[type_field].asnName:
                    idx_opaque = opaqueTypes[type_field].asnName.index(type_field_old)
                    is_opaque = True
        else:
            is_template = False

    [str_type, dim] = find_array_dim(type_field)

    #Raquel (it should be checked this
    if dim != '':
        type_field = str_type
        asn1_type += 'SEQUENCE(SIZE(1..' + dim + ')) OF '
    elif parameter != '':
        dim = parameter
    else:
        dim = '1'

    if type_field in basicTypes:
        asn1_type += basicTypes[type_field]
        if not basicTypes[type_field] in deps_types:
            deps_types.append(basicTypes[type_field])
    else:
        type_field = process_name_type(type_field)
        asn1_type += type_field
        if type_field not in deps_types:
            deps_types.append(type_field)

    return [asn1_type, deps_types, suffix, parameters, type_field, dim.replace('-','_'), is_opaque, idx_opaque]


def process_name_var(name):
    name = name.lower()
    name = name.replace('_', '-')
    name = name.replace('--', '-')
    if name.endswith('-'):
        name = name[0:-1]

    if name in invalidKeywords:
        name = name + '-val'
    return name


def process_name_type(name):
    name = name.replace('/','-')
    if name.startswith('-'):
        name = name[1:]

    name = name.replace('<-','<')

    # idx = name.rfind('<')
    # if isinstance(idx, int):
    #     name = name [0:idx+1] + name[idx+1].upper()+ name[idx+2:]

    sep = name.split('<')
    if len(sep)==1:
        name = name[0].upper() + name[1:]
    else:
        name = ''
        for i, s in enumerate(sep):
            if s != '':
                name += s[0].upper() + s[1:]
            if (i+1)!=len(sep):
                name += '<'


    #name = name[0].upper() + name[1:]
    name = name.replace('_', '-')
    name = name.replace('--','-')

    if name.endswith('-'):
        name = name[0:-1]

    if name in invalidKeywords:
        name = name + '-val'

    return name

def process_opaque(root):
    '''
    Process the nodes with the tag in the xml root
    :param root: tree root of xml file
    :return:
    '''

    for fields in root.findall('opaque'):
        name = fields.get('name')
        cpp_name = process_cpp_name(name)

        marshall = fields.get('marshal_as')
        cpp_marshall = process_cpp_name(marshall)
        name = process_name_type(name)
        marshall = process_name_type(marshall)

        if not marshall in opaqueTypes:
            opaqueTypes[marshall] = OpaqueType(name,cpp_name, marshall,cpp_marshall)

        else: #There exist two names marshalled as the same type
            opaqueTypes[marshall].add_new_name(name,cpp_name)

        cpp_include = process_cpp_include(fields)

        wrappers_includes = []
        for f in cpp_include:
            parts = f.split('/')

            # wrappers_include = 'orocos/' + parts[0] + '/wrappers/' #Commented
            wrappers_include = parts[0] + '/wrappers/'  # Commented

            for i in range(1, len(parts) - 1):
                wrappers_include += parts[i] + '/'
            wrappers_include += parts[-1]
            wrappers_includes.append(wrappers_include)

        opaqueTypes[marshall].cppInclude += cpp_include
        opaqueTypes[marshall].cppInclude += wrappers_includes
        opaqueTypes[marshall].cppInclude += process_orogen_include(fields)


        if not name in aliasTypes:
            aliasTypes[name] = marshall

        else:
            print('Problem')


def process_alias(root):
    '''
    Process the nodes with the tag in the xml root
    :param root: tree root of xml file
    :return:
    '''

    for fields in root.findall('alias'):
        name = fields.get('name')
        source = fields.get ('source')
        name = process_name_type(name)
        source = process_name_type(source)
        if not source in aliasTypes:
            aliasTypes[source] = name


def process_xml(root, tag):
    '''
    Process the nodes with the tag in the xml root
    :param root: tree root of xml file
    :param tag: tag to find in the tree xml
    :return:
    '''
    global sourceName, libName

    for fields in root.findall(tag):


        add_inst = False
        #name C++ of type
        name = fields.get('name')
        cpp_name = name

        #Capitalize() and replace _ by -
        name = process_name_type(name)

        add_container = False
        is_template = True

        #Check if the type is a template, only add the containers that have alias
        while is_template:
            if name in aliasTypes:
                name = aliasTypes[name]
                if tag == 'container':
                    add_container = True
            else:
                is_template = False

        [name2,type_template] = find_type_template(name)

        #if it is a template
        if type_template != '':
            type_template = process_name_type(type_template)

        #Obtain the source_file where the type will be defined
        parts = name2.split('-')
        source_file = parts[0].lower() + '.asn'
        #Obtain the library name
        name_source = process_name_type(parts[0])
        #hardcore the result ... all types in the same file
        name_source = libName

        source_file = sourceName


        #Obtain the name type in ASN1
        name_type = process_name_type(name2)

        #If it is template to change the name by the alias
        if type_template != '':
            is_template = True
            while is_template:
                if type_template in aliasTypes:
                    type_template = aliasTypes[type_template]
                else:
                    is_template = False

            name_type += '-' + process_name_type(type_template)

        # I don't know if it is necessary
        name_type = process_name_type(name_type)

        if tag == 'container' and add_container:
            name_type = name_type + 'P'#because is parametric

        # Initialize parameters of allTypes[name_type]
        if tag != 'container' or (tag == 'container' and add_container):
            if not name_type in allTypes:
                new_type = ConfigTypes(name_type)
                new_type.cppName = process_cpp_name(cpp_name)
                new_type.tag = tag
                # allTypes[name_type] = ConfigTypes(name_type)
                # allTypes[name_type].cppName = process_cpp_name(cpp_name)
                # allTypes[name_type].tag = tag

        asn_parameters = []
        sub_fields = []
        sub_types = []
        #cpp_name = name
        cpp_include = []
        suffix = []

        #Initialize the dependecies of other types and suffix(parameters)
        deps_types = []

        #if is a enum
        if tag == 'enum':
            str_type = name_type + " ::= ENUMERATED \n{\n"

            for grandson in fields:
                if grandson.tag == 'value':
                    subfields = grandson.attrib
                    symbol = subfields['symbol']
                    new_type.cppFields.append(symbol)
                    symbol = process_name_var(symbol)
                    #str_type += '\t' + symbol + '\t(' + subfields['value'] + '),\n'
                    str_type += '\t' + symbol + ',\n'
                    new_type.asnFields.append(symbol)
                    new_type.asn1SccFields.append(symbol.replace('-','_'))

            str_type = str_type[0:-2]  # Remove the las two characters because the last field does not finish in ','
            str_type += '\n}'

        elif tag == 'compound':
            str_type = ''#name_type + " ::= SEQUENCE \n{\n"

            for grandson in fields:
                if grandson.tag == 'field':
                    subfields = grandson.attrib
                    type_field = subfields['type']
                    new_type.cppTypes = type_field

                    type_field = process_name_type(type_field)

                    new_type.cppFields.append(subfields['name'])

                    name_var = process_name_var(subfields['name'])#+'-'+name_type)

                    new_type.asnFields.append(name_var)
                    new_type.asn1SccFields.append(name_var.replace('-','_'))
                    [asn1_type, deps_types_aux, suffix_aux, parameters_aux, root_type, dim, is_opaque, idx_opaque] = process_type_field(type_field,name_type+ '-'+name_var)
                    if parameters_aux:
                        new_type.asnParameters += parameters_aux
                        for p in parameters_aux:
                            new_type.asn1SccParameters.append(p.replace('-','_'))
                    if suffix_aux:
                        new_type.maxDim += suffix_aux

                    new_type.asnTypes.append(asn1_type)
                    new_type.rootTypes.append(root_type)
                    new_type.dimFields.append(dim)
                    new_type.isOpaque.append(is_opaque)
                    new_type.idxOpaque.append(idx_opaque)
                    new_type.depsTypes += deps_types_aux #Added al last

                    asn_parameters += parameters_aux

                    str_type += '\t' + name_var + '\t ' + asn1_type + ',\n'
                    deps_types += deps_types_aux
                    suffix += suffix_aux

            str_type = str_type[0:-2]  # Remove the las two characters because the last field does not finish in ','
            str_type += '\n}'

            str_suffix = ''
            if suffix:
                str_suffix = '{'
                for i, p in enumerate(suffix):
                    str_suffix += p
                    if (i+1) != len(suffix):
                        str_suffix += ', '
                str_suffix += '}'

            str_type = name_type + str_suffix + " ::= SEQUENCE \n{\n" + str_type
            if new_type.maxDim:
                add_inst = True
                name_type_inst = name_type
                name_type = name_type +'P'
                new_type.asnName = name_type
                # Definition of the inst
                if not name_type_inst in allTypes:
                    allTypes[name_type_inst] = ConfigTypes(name_type_inst)
                    allTypes[name_type_inst].cppName = process_cpp_name(cpp_name)
                    allTypes[name_type_inst].tag = 'inst'
                    allTypes[name_type_inst].rootTypes.append(name_type)
                    allTypes[name_type_inst].asnParameters = new_type.asnParameters
                    allTypes[name_type_inst].asn1SccParameters = new_type.asn1SccParameters
                    allTypes[name_type_inst].isOPaque = new_type.isOpaque
                    allTypes[name_type_inst].idxOPaque = new_type.isOpaque
                    allTypes[name_type_inst].depsTypes = new_type.depsTypes
                    #allTypes[name_type_inst].cppInclude = new_type.cppInclude

                    # Add an entry for such library
                    if not name_type_inst in libraries:
                        libraries[name_type_inst] = name_source + "-Types"



        elif tag == 'container' and add_container:
            name_type_inst = name_type[0:-1] #Remove P at the end
            [max_dim, parameter] = add_parameter_type(name_type_inst)

            new_type.maxDim.append(max_dim)
            if parameter:
                new_type.asnParameters.append (parameter)
                new_type.asn1SccParameters.append(parameter.replace('-','_'))
            str_type = name_type + "{T-UInt32: "+max_dim+"} ::= SEQUENCE (SIZE(1.."+max_dim+")) OF "

            container_type = fields.get ('of')
            new_type.cppTypes.append(container_type)

            container_type = process_name_type(container_type)

            [asn1_type, deps_types, suffix, parameters, root_type, dim, is_opaque, idx_opaque] = process_type_field(container_type)

            new_type.asnTypes.append(asn1_type)

            new_type.rootTypes.append(root_type)
            new_type.isOpaque.append(is_opaque)
            new_type.idxOpaque.append(idx_opaque)
            #Aqu/'i no hay parameters

            if suffix:
                print('Strange')

            str_type += asn1_type
            deps_types.append(parameter)
            deps_types.append('T-UInt32')

            #Added by Raquel
            new_type.depsTypes = deps_types

            asn_parameters.append(parameter)

            #Definition of the inst
            if not name_type_inst in allTypes:
                allTypes[name_type_inst] = ConfigTypes(name_type_inst)
                allTypes[name_type_inst].cppName = process_cpp_name(cpp_name)
                allTypes[name_type_inst].tag = 'inst'
                allTypes[name_type_inst].rootTypes.append(name_type)
                allTypes[name_type_inst].asnParameters.append(parameter)
                allTypes[name_type_inst].asn1SccParameters.append(parameter.replace('-','_'))
                allTypes[name_type_inst].isOpaque.append(is_opaque)
                allTypes[name_type_inst].idxOpaque.append(idx_opaque)
                allTypes[name_type_inst].depsTypes += deps_types
                #allTypes[name_type_inst].cppInclude = new_type.cppInclude
                add_inst = True

                # Add an entry for such library
                if not name_type_inst in libraries:
                    libraries[name_type_inst] = name_source + "-Types"

        # Initialize parameters of allTypes[name_type]
        if tag != 'container' or (tag == 'container' and add_container):
            if not name_type in allTypes:
                allTypes[name_type] = new_type

            # if not name_type in aliasTypes:
            #     aliasTypes[name_type] = name_type + "{"+parameter+"}"

        # Add an entry for such library
        if not name_type in libraries:
            libraries[name_type] = name_source + "-Types"

        if tag != 'container' or (tag == 'container' and add_container):

            #if not name_type in allTypes:
                #allTypes[name_type] = ConfigTypes(name_type)
                #allTypes[name_type].asnParameters = asn_parameters
                #allTypes[name_type].cppName = cpp_name
                #allTypes[name_type].cppInclude = cpp_include
                #allTypes[names].tag = tag
                #allTypes.append(name_type)
            if not source_file in allInfo:
                allInfo[source_file] = AsnFile(name_source)

            allInfo[source_file].strTypes.append(str_type)
            allInfo[source_file].nameTypes.append(name_type)


            for deps in deps_types:
                if deps not in allInfo[source_file].depsTypes:
                    allInfo[source_file].depsTypes.append(deps)

            #Process cpp includes
            cpp_includes =  process_cpp_include(fields)
            orogen_includes = process_orogen_include(fields)
            allTypes[name_type].cppInclude =cpp_includes+orogen_includes

            if add_inst:
                allInfo[source_file].nameTypes.append(name_type_inst)
                allInfo[source_file].strTypes.append('')  # esto no har/'ia falta
                allTypes[name_type_inst].cppInclude =cpp_includes+orogen_includes
                add_inst = False


            #print str_type
def process_cpp_include(fields):
    cpp_includes = []
    # Process cpp includes
    for subfields in fields.findall('metadata'):
        key = subfields.get('key')
        # if key == 'orogen_include':
        if key == 'source_file_line':
            cpp_include = subfields.text
            parts = cpp_include.split(':')
            # cpp_include = parts[-1]
            cpp_include = parts[0]

            include_orocos = True
            for f in includePath:
                idx = cpp_include.rfind(f)

                if idx == 0:
                    include_orocos = False
                    cpp_include = cpp_include[len(f):-1]+cpp_include[-1]
                    #cpp_include = cpp_include.lstrip(f)
                    break
                    # If there is no in cmake_prefix_path, include orocos/....
            if include_orocos:
                parts = cpp_include.split('/types/')
                cpp_include = parts[-1]
                #cpp_include = 'orocos/' + cpp_include Comment before experiment

            cpp_includes.append(cpp_include)
    return cpp_includes

def process_orogen_include(fields):
    cpp_includes = []
    # Process cpp includes
    for subfields in fields.findall('metadata'):
        key = subfields.get('key')
        # if key == 'orogen_include':
        if key == 'orogen_include':
            cpp_include = subfields.text
            parts = cpp_include.split(':')
            # cpp_include = parts[-1]
            cpp_include = parts[-1]

            cpp_includes.append(cpp_include)
    return cpp_includes

def find_libraries(deps_types, pkg_name):
    import_libraries = dict()
    same_lib = pkg_name + '-Types'
    if deps_types:
        for t in deps_types:
            if t in libraries:
                lib = libraries[t]
                if lib != same_lib:
                    if not lib in import_libraries:
                        import_libraries[lib] = []
                    import_libraries[lib].append(t)
    return import_libraries

def add_parameter_type(name_type):

    source_file = userDefsSource
    deps = 'T-UInt32'

    max_dim = 'max' + name_type

    parameter = 'num' +name_type

    str_type = parameter + '\t'+ deps +" ::= 200 "

    allInfo[source_file].strTypes.append(str_type)
    allInfo[source_file].nameTypes.append(parameter)

    if not parameter in libraries:
        libraries[parameter] = userDefsLib + "-Types"

    if deps not in allInfo[source_file].depsTypes:
        allInfo[source_file].depsTypes.append (deps)
    return [max_dim, parameter]

def add_var_type(name_type):

    source_file = userDefsSource
    deps = 'T-UInt32'

    num_name_type = 'max' + name_type

    str_type = num_name_type + " ::= 200 "+deps

    allInfo[source_file].strTypes.append (str_type)
    allInfo[source_file].nameTypes.append (num_name_type)

    if deps not in allInfo[source_file].depsTypes:
        allInfo[source_file].depsTypes.append (deps)
    return num_name_type

def process_cpp_name(cpp_name):
    cpp_name = cpp_name.replace('/', '::')
    cpp_name = cpp_name.lstrip('::')
    cpp_name = cpp_name.replace('<::','<')
    return cpp_name

def main():
    global sourceName, libName, userDefsSource, userDefsLib
    options = parse_args()

    file_tlb = options[0]

    source_name = file_tlb.split('/')
    source_name = source_name[-1]
    source_name = source_name.rstrip('.tlb')
    name_lib = source_name.capitalize()
    userDefsSource = 'userdefs-' + source_name + '.asn'
    userDefsLib = 'UserDefs-' + name_lib
    source_name = source_name + '.asn'

    sourceName = source_name
    libName = name_lib

    out_asn = options[1]
    out_support = options[2]

    tree = ET.parse(file_tlb)
    root = tree.getroot()



    # Find all numeric types

    for numeric_types in root.findall('numeric'):
        names = numeric_types.get('name')
        cpp_name = names.strip('/')
        cpp_include =[]
        names = process_name_type(names)
        #names = names.strip('/')
        if names in basicTypes:
            print (names, basicTypes[names])
            if not basicTypes[names] in allTypes:
                allTypes[names] = ConfigTypes(basicTypes[names])
                allTypes[names].cppName = process_cpp_name(cpp_name)
                allTypes[names].tag = 'numeric'

                for subfields in numeric_types.findall('metadata'):
                    key = subfields.get('key')
                    if key == 'orogen_include':
                        cpp_include.append(subfields.text)
                allTypes[names].cppInclude = cpp_include
        else:

            print('Does not exist this basic type')

    allInfo[userDefsSource] = AsnFile(userDefsLib)

    allInfo[userDefsSource].nameTypes.append('Dummy'+libName+'-T')
    allInfo[userDefsSource].strTypes.append('Dummy'+libName+'-T ::= T-UInt32')
    libraries['Dummy'+libName+'-T'] = userDefsLib + '-Types'

    #Soluci/'on temporal
    cpp_name = '/std/string'
    cpp_name = cpp_name.strip('/')
    name = 'Std-string'
    cpp_include =[]
    allTypes[name] = ConfigTypes(basicTypes[name])


    if not basicTypes[name] in allTypes:
        name = 'T-String'

        new_type = ConfigTypes(name)
        new_type.cppName = process_cpp_name(cpp_name)
        new_type.tag = 'inst'
        #Faltar/'ia include cpp includes

        #[max_dim, parameter] = add_parameter_type('T-String')
        max_dim = 'maxT-String'
        parameter = 'numT-String'

        new_type.maxDim.append(max_dim)

        new_type.asnParameters.append(parameter)
        new_type.asn1SccParameters.append(parameter.replace('-','_'))
        new_type.rootTypes.append('T-StringP')

        allTypes['T-StringP'] = ConfigTypes('T-StringP')
        allTypes['T-StringP'].asnParameters.append(parameter)

        # Added by Raquel
        new_type.depsTypes.append(parameter)
        new_type.depsTypes.append('T-UInt32')
        allTypes['Std-string'] = new_type
        allTypes['T-String'] = new_type

    else:
        print('Does not exist this basic type')




    allInfo[sourceName] = AsnFile(libName)
    allInfo[sourceName].nameTypes.append('Dummy2'+libName+'-T')
    allInfo[sourceName].strTypes.append('Dummy2'+libName+'-T ::= Dummy'+libName+'-T')
    allInfo[sourceName].depsTypes.append('Dummy'+libName+'-T')
    libraries['Dummy2'+libName+'-T'] = libName+'-Types'

    #allInfo['userdefs.asn'].nameTypes.append('numT-String')
    #allInfo['userdefs.asn'].strTypes.append('numT-String T-UInt32 ::= 200')
    #libraries['numT-String'] = 'UserDefs-Types'

    process_opaque(root)

    process_alias(root)

    process_xml(root, 'enum')

    process_xml (root, 'container')

    process_xml(root, 'compound')

    asn_template = Template(filename="template.asn.mako")

    if not os.path.exists(out_asn):
        os.makedirs(out_asn)



    #Added by Raquel
    for k in allInfo:
        pkg = allInfo[k]
        for t in pkg.nameTypes:
            if t in allTypes:
                deps_types = allTypes[t].depsTypes
                for deps in deps_types:
                    if deps in allTypes:
                        deps_types2 = allTypes[deps].depsTypes
                        for d in deps_types2:
                            if d not in allInfo[k].depsTypes:
                                allInfo[k].depsTypes.append(d)

    # #Instanciar new Types
    # for k in allInfo:
    #     pkg = allInfo[k]:
    #     for t in pkg.nameTypes:
    #         if t in allTypes:
    #             if t.asnParameters:
    #                 #Add type
    #                 newType =

    generated_files = ['taste-extended', 'taste-types']

    for k in allInfo:
        asn_file=k.split('.')
        asn_file=asn_file[0]
        generated_files.append(asn_file)
        pkg = allInfo[k]
        buf = StringIO()
        pkg_libs = find_libraries(pkg.depsTypes, pkg.name)
        ctx = Context(buf, config=pkg, librariesConfig=pkg_libs, configTypes=allTypes)
        asn_template.render_context(ctx)
        name_file = os.path.join(out_asn, k)
        f = open(name_file, 'w')
        f.write(buf.getvalue())
        f.close()
    copyfile('taste-types.asn', os.path.join(out_asn, 'taste-types.asn'))
    copyfile('taste-extended.asn', os.path.join(out_asn, 'taste-extended.asn'))

    hpp_template = Template(filename="template_convert.hpp.mako")
    cpp_template = Template(filename="template_convert.cpp.mako")
    h_template = Template(filename="template_types.h.mako")
    hpp_convert_template = Template(filename="opaque_convert.hpp.mako")
    cpp_convert_template = Template(filename="opaque_convert.cpp.mako")

    buf = StringIO()
    ctx = Context(buf, root='BASE', generated_files=generated_files)
    h_template.render_context(ctx)
    name_file = os.path.join(out_support, 'baseTypes.h')
    f = open(name_file, 'w')
    f.write(buf.getvalue())
    f.close()

    for t in allTypes:
        type_info = allTypes[t]
        buf = StringIO()
        if type_info.tag != 'numeric':

            if not type_info.asnParameters or type_info.tag == 'inst':



                define_name = type_info.asnName.upper()
                define_name = define_name.replace('-','_')+'_CONVERT'

                deps_include = [];

                if type_info.tag != 'inst':

                    for d in allTypes[t].depsTypes:
                        if d in allTypes:
                            if allTypes[d].tag != 'numeric':
                                deps_include.append(d + 'Convert.hpp')
                else:
                    root_type = allTypes[t].rootTypes[0]
                    for d in allTypes[root_type].depsTypes:
                        if d in allTypes:
                            if allTypes[d].tag != 'numeric':
                                deps_include.append(d + 'Convert.hpp')

                if type_info.tag == 'inst':
                    ctx = Context(buf, config=type_info, name=define_name, all_info=allTypes, includeConvert=deps_include,opaqueTypes=opaqueTypes)
                else:
                    ctx = Context(buf, config=type_info, name=define_name, all_info=allTypes, includeConvert=deps_include)
                hpp_template.render_context(ctx)
                name_file = os.path.join(out_support, t+'Convert.hpp')
                f = open(name_file, 'w')
                f.write(buf.getvalue())
                f.close()




                #Cpp Convert
                if type_info.tag != 'inst':
                    buf = StringIO()
                    ctx = Context(buf, config=type_info, includeName =t+'Convert.hpp', all_info=allTypes, basic_info=basicTypes, includeConvert=deps_include, opaqueTypes=opaqueTypes)
                    cpp_template.render_context(ctx)
                    name_file = os.path.join(out_support, t + 'Convert.cpp')
                    f = open(name_file, 'w')
                    f.write(buf.getvalue())
                    f.close()


    #Creation of OpaqueConversion.hpp
    cpp_includes=[]
    for t in opaqueTypes:
        opaque_info = opaqueTypes[t]
        for f2 in opaque_info.cppInclude:
            if not f2 in cpp_includes:
                cpp_includes.append(f2)

    buf = StringIO()
    ctx = Context(buf, opaqueTypes=opaqueTypes,cppIncludes=cpp_includes)
    hpp_convert_template.render_context(ctx)
    name_file = os.path.join(out_support, 'OpaqueConversion.hpp')
    f = open(name_file, 'w')
    f.write(buf.getvalue())
    f.close()

    # Creation of OpaqueConversion.hpp

    name_file = os.path.join(out_support, 'OpaqueConversion.cpp')
    if not os.path.isfile(name_file):
        buf = StringIO()
        ctx = Context(buf, opaqueTypes=opaqueTypes)
        cpp_convert_template.render_context(ctx)
        f = open(name_file, 'w')
        f.write(buf.getvalue())
        f.close()


if __name__ == '__main__':
    main()
