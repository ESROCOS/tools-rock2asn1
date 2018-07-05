/*
 * Intermediate conversion functions.
 */

#ifndef OPAQUE_CONVERSION_H
#define OPAQUE_CONVERSION_H

%for f in cppIncludes:
%if f.find('rtt')!=-1:
# if defined( __GNUC__ ) && defined( __sparc__ ) 
#  warning Compiling for SPARC, but temporarily defining __i386__ to trick RTT to compile the headers (see rtt-config.h)
#  define __i386__
#  ifndef PTHREAD_MUTEX_RECURSIVE_NP
#   warning Defining PTHREAD_MUTEX_RECURSIVE_NP, needed by RTT headers
#   define PTHREAD_MUTEX_RECURSIVE_NP PTHREAD_MUTEX_RECURSIVE
#  endif
#include <${f}>
#  undef __i386__
# else
#include <${f}>
# endif
%else:
#include <${f}>
%endif
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
