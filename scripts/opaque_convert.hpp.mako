/*
 * H2020 ESROCOS Project
 * Company: GMV Aerospace & Defence S.A.U.
 * Licence: GPLv2
 */

/*
 * Intermediate conversion functions.
 */

#ifndef OPAQUE_CONVERSION_H
#define OPAQUE_CONVERSION_H


%for f in cppIncludes:
#include <${f}>
%endfor

//Conversion functions from the instanced type to the marshaled type

%for t in opaqueTypes:
<%opaque_info=opaqueTypes[t]%>
%for n in opaque_info.asnName:
void ${opaque_info.briefName[loop.index]}_fromIntermediate(${opaque_info.cppName[loop.index]}& result, const ${opaque_info.cppMarshall}& cppMarshall);

void ${opaque_info.briefName[loop.index]}_toIntermediate(${opaque_info.cppMarshall}& result, const ${opaque_info.cppName[loop.index]}& cppVal);
%endfor
%endfor

#endif //OPAQUE_CONVERSION_H