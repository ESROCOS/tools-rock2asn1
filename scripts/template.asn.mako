${config.name}-Types DEFINITIONS ::=
BEGIN

%if librariesConfig:
IMPORTS\
%for lib in librariesConfig:
%for t in librariesConfig[lib]:
%if not loop.last:
 ${t},\
%else:
 ${t}\
%endif
%endfor
 FROM ${lib}\
%endfor
;
%endif

%for t in config.nameTypes:
<%i = loop.index%>\
--Definition ${t} starts
%if t in configTypes:
%if configTypes[t].tag == 'enum':
${configTypes[t].asnName} ::= ENUMERATED
{
%for s in configTypes[t].asnFields:
%if not loop.last:
    ${s},
%else:
    ${s}
%endif
%endfor
}
%elif configTypes[t].tag == 'container' :
${configTypes[t].asnName} {T-UInt16: ${configTypes[t].maxDim[0]}} ::= SEQUENCE(SIZE(1..${configTypes[t].maxDim[0]})) OF ${configTypes[t].asnTypes[0]}
%elif configTypes[t].tag == 'compound':
${configTypes[t].asnName}\
%if configTypes[t].maxDim:
{\
%for d in configTypes[t].maxDim:
%if not loop.last:
T-UInt32: ${d}, \
%else:
T-UInt32: ${d}\
%endif
%endfor
}\
%endif
 ::= SEQUENCE
{
%for f in configTypes[t].asnFields:
<%root_type = configTypes[t].rootTypes[loop.index]%>\
    ${f}  ${configTypes[t].asnTypes[loop.index]}\
##%if root_type in configTypes:
##%if configTypes[root_type].asnParameters:
##{\
##%for p in configTypes[root_type].asnParameters:
##${p}\
##%if not loop.last:
##, \
##%else:
##}\
##%endif
##%endfor
##%endif
##%endif
%if not loop.last:
,
%else:

%endif
%endfor
}
%elif configTypes[t].tag == 'inst' :
${configTypes[t].asnName} ::= ${configTypes[t].rootTypes[0]}\
%if configTypes[t].asnParameters:
{\
%for p in configTypes[t].asnParameters:
${p}\
%if not loop.last:
, \
%endif
%endfor
}\
%endif

%endif
%else:
    ${config.strTypes[loop.index]}
%endif
-- Definition ${t} ends

%endfor

END