
#include "test_frame.hpp"

bool test_frame(void)
{   
    using namespace base::samples::frame;
    base::samples::frame::frame_mode_t mode = base::samples::frame::MODE_BAYER;
    base::samples::frame::Frame cppOrigin(480,680);
    bool success = true;
    
    
    cppOrigin.setFrameMode(mode);
    std::cout << "Mode set cppOrigin" << mode << std::endl;
    base::samples::frame::Frame cppDest;
    asn1SccBase_samples_frame_Frame asnVal;
    
    asn1SccBase_samples_frame_Frame_toAsn1(asnVal, cppOrigin);
    
    //std::cout << "Mode asn1: "<< asnVal.frame_mode << std::endl;

    if (asnVal.frame_mode != asn1Sccbase_samples_frame_frame_mode_t_mode_bayer)
    {
        success = false;
    }

    //asnVal.frame_mode =asn1Sccmode_bayer;
    
    asn1SccBase_samples_frame_Frame_fromAsn1(cppDest, asnVal);
    
    
    if (cppDest.getFrameMode()!=cppOrigin.getFrameMode())
    {
        success = false;
    }
    
    return (success);
}
