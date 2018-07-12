#include "Base-samples-frame-FrameConvert.hpp"
#include <iostream>

#ifndef _INC_DATAVIEW_UNIQ_H
#ifndef GENERATED_ASN1_DATAVIEW_UNIQ_H
#ifndef GENERATED_ASN1SCC_DATAVIEW_UNIQ_H
#ifndef GENERATED_ASN1SCC_dataview_uniq_H

#include "asn1/asn1crt.h"
#include "asn1/taste-extended.h"
#include "asn1/taste-types.h"
#include "asn1/userdefs-base.h"
#include "asn1/base.h"

#endif //GENERATED_ASN1SCC_dataview_uniq_H
#endif //GENERATED_ASN1SCC_DATAVIEW_UNIQ_H
#endif //GENERATED_ASN1_DATAVIEW_UNIQ_H
#endif //_INC_DATAVIEW_UNIQ_H



int main()
{
    base::samples::frame::frame_mode_t mode = base::samples::frame::MODE_BAYER;
    base::samples::frame::Frame cppOrigin(480,680);
    cppOrigin.setFrameMode(mode);
    std::cout << "Mode set cppOrigin" << mode << std::endl;
    base::samples::frame::Frame cppDest;
    asn1SccBase_samples_frame_Frame asnVal;
    
    asn1SccBase_samples_frame_Frame_toAsn1(asnVal, cppOrigin);
    std::cout << "Mode asn1: "<< asnVal.frame_mode << std::endl;
    //asnVal.frame_mode =asn1Sccmode_bayer;
    
    asn1SccBase_samples_frame_Frame_fromAsn1(cppDest, asnVal);
    
    std::cout << "Mode set cppdest" << cppDest.getFrameMode() << std::endl;
    if (cppDest.getFrameMode()==cppOrigin.getFrameMode())
    {
        std::cout << "Test done succesfully"<< std::endl; 
    }
    else
    {
        std::cout<< "Test done unsuccessfully" << std::endl;
    }
    
}
