
#include "${includeName}"

#include "OpaqueConversion.hpp"

%for f in includeConvert:
#include "${f}"
%endfor
//Conversion functions from asn1 to c++ type



void ${config.asn1SccName}_fromAsn1(${config.cppName}& result, const ${config.asn1SccName}& asnVal)
{
%if config.tag == 'enum':
    result = (${config.cppName}) asnVal;

%elif config.tag == 'container':
    for (int i = 0; i < ${config.asn1SccParameters[0]}; i++)
    {
        result[i] = asnVal.arr[i];
    }

%elif config.tag == 'compound':
%for f in config.cppFields:
<% root_type = all_info[config.rootTypes[loop.index]]%>\
%if root_type.tag == 'numeric' and config.dimFields[loop.index] == '1':
    result.${f} = asnVal.${config.asn1SccFields[loop.index]};
%elif root_type.tag == 'numeric' and config.dimFields[loop.index]!='1':
    for(int i = 0; i < ${config.dimFields[loop.index]};i++)
    {
        result.${f}[i] = asnVal.${config.cppFields[loop.index]}.arr[i];
    }
%elif root_type.tag != 'numeric' and config.dimFields[loop.index]== '1':
%if config.isOpaque[loop.index]:
<%opaque_info = opaqueTypes[root_type.asnName]%>
    ${opaque_info.cppMarshall} ${f}_intermediate;
    ${root_type.asn1SccName}_fromAsn1(${f}_intermediate, asnVal.${config.asn1SccFields[loop.index]});
    ${opaque_info.briefName[config.idxOpaque[loop.index]]}_fromIntermediate(result.${f}, ${f}_intermediate);
%else:
    ${root_type.asn1SccName}_fromAsn1(result.${f}, asnVal.${config.asn1SccFields[loop.index]});
%endif
%elif  root_type.tag != 'numeric' and config.dimFields[loop.index]!= '1':
    for(int i = 0; i < ${config.dimFields[loop.index]};i++)
    {
        ${root_type.asn1SccName}_fromAsn1(result.${f}[i], asnVal.${config.asn1SccFields[loop.index]}.arr[i]);
    }
%endif

%endfor
%endif
}

//Conversion functions from c++ type to asn1

void ${config.asn1SccName}_toAsn1(${config.asn1SccName}& result, const ${config.cppName}& baseObj)
{
%if config.tag == 'enum':
    result = (${config.asn1SccName}) baseObj;

%elif config.tag == 'container':
    for (int i = 0; i < ${config.asn1SccParameters[0]}; i++)
    {
        result.arr[i] = baseObj[i];
    }

%elif config.tag == 'compound':
%for f in config.cppFields:
<% root_type = all_info[config.rootTypes[loop.index]]%>\
%if root_type.tag == 'numeric' and config.dimFields[loop.index] == '1':
    result.${config.asn1SccFields[loop.index]} = baseObj.${f};
%elif root_type.tag == 'numeric' and config.dimFields[loop.index]!='1':
    for(int i = 0; i < ${config.dimFields[loop.index]};i++)
    {
        result.${config.cppFields[loop.index]}.arr[i] = baseObj.${f}[i];
    }
%elif root_type.tag != 'numeric' and config.dimFields[loop.index]== '1':
%if config.isOpaque[loop.index]:
<%opaque_info = opaqueTypes[root_type.asnName]%>
    ${opaque_info.cppMarshall} ${f}_intermediate;
    ${opaque_info.briefName[config.idxOpaque[loop.index]]}_toIntermediate(${f}_intermediate, baseObj.${f});
    ${root_type.asn1SccName}_toAsn1(result.${config.asn1SccFields[loop.index]}, ${f}_intermediate);
%else:
    ${root_type.asn1SccName}_toAsn1(result.${config.asn1SccFields[loop.index]}, baseObj.${f});
%endif
%elif  root_type.tag != 'numeric' and config.dimFields[loop.index]!= '1':
    for(int i = 0; i < ${config.dimFields[loop.index]};i++)
    {
        ${root_type.asn1SccName}_toAsn1(result.${config.asn1SccFields[loop.index]}.arr[i], baseObj.${f}[i]);f
    }
%endif

%endfor
%endif
}


