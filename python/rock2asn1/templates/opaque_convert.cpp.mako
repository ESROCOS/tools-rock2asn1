
#include "OpaqueConversion.hpp"


//Conversion functions from the instanced type to the marshaled type

%for t in opaqueTypes:
<%opaque_info=opaqueTypes[t]%>
%for n in opaque_info.asnName:
void ${opaque_info.briefName[loop.index]}_fromIntermediate(${opaque_info.cppName[loop.index]}& result, const ${opaque_info.cppMarshall}& cppMarshall)
{
    /*Add user code for this conversion*/
}

void ${opaque_info.briefName[loop.index]}_toIntermediate(${opaque_info.cppMarshall}& result, const ${opaque_info.cppName[loop.index]}& cppval)
{
    /*Add user code for this conversion*/
}

%endfor
%endfor




