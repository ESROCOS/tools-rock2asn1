/*
 * H2020 ESROCOS Project
 * Company: GMV Aerospace & Defence S.A.U.
 * Licence: GPLv2
 */

/*
 * A header file to import all the asn1 types either from the
 * types library or from dataview-uniq.h (if building from TASTE).
 */

#ifndef ${root}TYPES_HPP
#define ${root}TYPES_HPP

// Include types generated from ASN.1. These are either:
// - in dataview-uniq.h, if building from TASTE
//   (IMPORTANT: note that the order of includes matters)
// - in the asn1, if building from outside TASTE
// We distingush between the two cases by checking the include variable
#ifndef _INC_DATAVIEW_UNIQ_H
#ifndef GENERATED_ASN1_DATAVIEW_UNIQ_H
#ifndef GENERATED_ASN1SCC_DATAVIEW_UNIQ_H

#include "asn1/asn1crt.h"
%for f in generated_files:
#include "asn1/${f}.h"
%endfor

#endif //GENERATED_ASN1SCC_DATAVIEW_UNIQ_H
#endif //GENERATED_ASN1_DATAVIEW_UNIQ_H
#endif //_INC_DATAVIEW_UNIQ_H

#endif //BASETYPES_HPP