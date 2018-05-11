/*
 * H2020 ESROCOS Project
 * Company: GMV Aerospace & Defence S.A.U.
 * Licence: GPLv2
 */

/*
 * Conversion functions for ${config.asn1SccName}.
 */

#ifndef ${name}
#define ${name}

#include "baseTypes.h"
%for f in config.cppInclude:
#include <${f}>
%endfor
#include <string.h>
#include <stdio.h>

%for f in includeConvert:
#include "${f}"
%endfor


//Conversion functions from asn1 to c++ type
%if config.tag == 'inst':
<%root_type = all_info[config.rootTypes[0]]%>
template <typename T>
void ${config.asn1SccName}_fromAsn1(${config.cppName}& result, const T & asnVal,\
%for p in config.asn1SccParameters:
    asn1SccT_UInt32 length_${p}=${p}\
    %if not loop.last:
, \
    %endif
%endfor
)
{

%if root_type.asnName == 'T-StringP':
    char cstr[length_${config.asn1SccParameters[0]}+1];

    memcpy(cstr, asnVal.arr,asnVal.nCount);
    cstr[asnVal.nCount] = '\0';

    result = std::string(cstr);


%elif root_type.tag == 'container':
<% root_type_field = all_info[root_type.rootTypes[0]]%>\
    result.resize(asnVal.nCount);
    for (int i = 0; i < length_${config.asn1SccParameters[0]}; i++)
    {
%if root_type_field == 'numeric':
        result[i] = asnVal.arr[i];
%elif  root_type.isOpaque[0]:
<%opaque_info = opaqueTypes[root_type_field.asnName]%>\
		${opaque_info.cppMarshall} ${f}_intermediate;
		${root_type_field.asn1SccName}_fromAsn1(${f}_intermediate, asnVal.arr[i]);
		${opaque_info.briefName[root_type.idxOpaque[0]]}_fromIntermediate(result[i], ${f}_intermediate);
%else:
		${root_type_field.asn1SccName}_fromAsn1(result[i], asnVal.arr[i]);
%endif
    }
%elif root_type.tag == 'compound':
%for f in root_type.cppFields:
<% root_type_field = all_info[root_type.rootTypes[loop.index]]%>\
%if root_type_field.tag == 'numeric' and root_type.dimFields[loop.index] == '1':
    result.${f} = asnVal.${root_type.asn1SccFields[loop.index]};
%elif root_type_field.tag == 'numeric' and root_type.dimFields[loop.index]!='1':
    result.${f}.resize(asnVal.${root_type.asn1SccFields[loop.index]}.nCount);
    for(int i = 0; i < ${root_type.dimFields[loop.index]};i++)
    {
        result.${f}[i] = asnVal.${root_type.asn1SccFields[loop.index]}.arr[i];
    }
%elif root_type_field.tag != 'numeric' and root_type.dimFields[loop.index]== '1':
%if root_type.isOpaque[loop.index]:
<%opaque_info = opaqueTypes[root_type_field.asnName]%>\
    ${opaque_info.cppMarshall} ${f}_intermediate;
    ${root_type_field.asn1SccName}_fromAsn1(${f}_intermediate, asnVal.${root_type.asn1SccFields[loop.index]});
    ${opaque_info.briefName[root_type.idxOpaque[loop.index]]}_fromIntermediate(result.${f}, ${f}_intermediate);
%else:
    ${root_type_field.asn1SccName}_fromAsn1(result.${f}, asnVal.${root_type.asn1SccFields[loop.index]});
%endif
%elif  root_type_field.tag != 'numeric' and root_type.dimFields[loop.index]!= '1':
    result.${f}.resize(asnVal.${root_type.asn1SccFields[loop.index]}.nCount);
    for(int i = 0; i < ${root_type.dimFields[loop.index]};i++)
    {
%if root_type.isOpaque[loop.index]:
<%opaque_info = opaqueTypes[root_type_field.asnName]%>\
		${opaque_info.cppMarshall} ${f}_intermediate;
		${root_type_field.asn1SccName}_fromAsn1(${f}_intermediate, asnVal.${root_type.asn1SccFields[loop.index]}.arr[i]);
		${opaque_info.briefName[root_type.idxOpaque[loop.index]]}_fromIntermediate(result.${f}[i], ${f}_intermediate);
%else:
        ${root_type_field.asn1SccName}_fromAsn1(result.${f}[i], asnVal.${root_type.asn1SccFields[loop.index]}.arr[i]);
%endif
    }
%endif

%endfor
%endif
}
%else:
void ${config.asn1SccName}_fromAsn1(${config.cppName}& result, const ${config.asn1SccName}& asnVal);
%endif

//Conversion functions from C++ to Asn1 type
%if config.tag == 'inst':
<%root_type = all_info[config.rootTypes[0]]%>
template <typename T>
void ${config.asn1SccName}_toAsn1(T & result, const ${config.cppName}& baseObj,\
%for p in config.asn1SccParameters:
    asn1SccT_UInt32 length_${p}=${p}\
    %if not loop.last:
, \
    %endif
%endfor
)
{

%if root_type.asnName == 'T-StringP':
     // Limit length to the maximum supported

    asn1SccT_UInt32 len = strlen(baseObj.c_str());
    if (len+1 > length_${config.asn1SccParameters[0]})
    {
        len = length_${config.asn1SccParameters[0]}-1;
        fprintf(stderr, "WARNING: string truncated to %lld characters.\n",length_${config.asn1SccParameters[0]} );
    }

    memcpy(result.arr, baseObj.c_str() , len);
    result.nCount = len;
    result.arr[len]='\0';

%elif root_type.tag == 'container':
<% root_type_field = all_info[root_type.rootTypes[0]]%>\
    for (int i = 0; i < length_${config.asn1SccParameters[0]}; i++)
    {
%if root_type_field == 'numeric':
        result.arr[i] = baseObj[i];
%elif  root_type.isOpaque[0]:
<%opaque_info = opaqueTypes[root_type_field.asnName]%>\
		${opaque_info.cppMarshall} ${f}_intermediate;
		${opaque_info.briefName[root_type.idxOpaque[0]]}_toIntermediate(${f}_intermediate, baseObj[i]);
		${root_type_field.asn1SccName}_toAsn1(result.arr[i], ${f}_intermediate);

%else:
		${root_type_field.asn1SccName}_toAsn1(result.arr[i], baseObj[i]);
%endif

    }
    result.nCount = length_${config.asn1SccParameters[0]};
%elif root_type.tag == 'compound':
%for f in root_type.cppFields:
<% root_type_field = all_info[root_type.rootTypes[loop.index]]%>\
%if root_type_field.tag == 'numeric' and root_type.dimFields[loop.index] == '1':
    result.${root_type.asn1SccFields[loop.index]} = baseObj.${f};
%elif root_type_field.tag == 'numeric' and root_type.dimFields[loop.index]!='1':
    for(int i = 0; i < ${root_type.dimFields[loop.index]};i++)
    {
        result.${root_type.asn1SccFields[loop.index]}.arr[i]= baseObj.${f}[i];
    }
%elif root_type_field.tag != 'numeric' and root_type.dimFields[loop.index]== '1':
%if root_type.isOpaque[loop.index]:
<%opaque_info = opaqueTypes[root_type_field.asnName]%>\
    ${opaque_info.cppMarshall} ${f}_intermediate;
    ${opaque_info.briefName[root_type.idxOpaque[loop.index]]}_toIntermediate(${f}_intermediate, baseObj.${f});
    ${root_type_field.asn1SccName}_toAsn1(result.${root_type.asn1SccFields[loop.index]}, ${f}_intermediate);
%else:
    ${root_type_field.asn1SccName}_toAsn1(result.${root_type.asn1SccFields[loop.index]}, baseObj.${f});
%endif
%elif  root_type_field.tag != 'numeric' and root_type.dimFields[loop.index]!= '1':
    for(int i = 0; i < ${root_type.dimFields[loop.index]};i++)
    {
%if root_type.isOpaque[loop.index]:
<%opaque_info = opaqueTypes[root_type_field.asnName]%>\
		${opaque_info.cppMarshall} ${f}_intermediate;
		${opaque_info.briefName[root_type.idxOpaque[loop.index]]}_fromIntermediate(${f}_intermediate, baseObj.${f}[i]);
		${root_type_field.asn1SccName}_toAsn1(result.${root_type.asn1SccFields[loop.index]}.arr[i], ${f}_intermediate);
%else:
        ${root_type_field.asn1SccName}_toAsn1(result.${root_type.asn1SccFields[loop.index]}.arr[i], baseObj.${f}[i]);
%endif
    }
%endif

%endfor
%endif
}
%else:
void ${config.asn1SccName}_toAsn1(${config.asn1SccName}& result, const ${config.cppName}& baseObj);
%endif


#endif //${name}
