/*
 * H2020 ESROCOS Project
 * Company: GMV Aerospace & Defence S.A.U.
 * Licence: GPLv2
 */
 
#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MAIN
#include "Base-samples-frame-FrameConvert.hpp"
#include "Base-JointStateConvert.hpp"
#include <iostream>
#include <boost/test/unit_test.hpp>

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

//#define BOOST_TEST_MAIN

//#define BOOST_TEST_MODULE(test_frame)


BOOST_AUTO_TEST_CASE(test_frame)
{   
    using namespace base::samples::frame;
    base::samples::frame::frame_mode_t mode = base::samples::frame::MODE_BAYER;
    base::samples::frame::Frame cppOrigin(480,680);
    bool success = true;
    
    
    cppOrigin.setFrameMode(mode);
    //std::cout << "Mode set cppOrigin " << mode << std::endl;
    base::samples::frame::Frame cppDest;
    asn1SccBase_samples_frame_Frame asnVal;
    
    asn1SccBase_samples_frame_Frame_toAsn1(asnVal, cppOrigin);
    
    //std::cout << "Mode asn1: "<< asnVal.frame_mode << std::endl;
    
    BOOST_CHECK_EQUAL(asnVal.frame_mode, asn1Sccbase_samples_frame_frame_mode_t_mode_bayer);

    
    asn1SccBase_samples_frame_Frame_fromAsn1(cppDest, asnVal);
    
    BOOST_CHECK_EQUAL(cppDest.getFrameMode(), cppOrigin.getFrameMode());
}

BOOST_AUTO_TEST_CASE(test_JointState)
{
    base::JointState cppOrigin; //by default the mode is UNSET
    base::JointState cppDest;
    asn1SccBase_JointState asnVal;
    cppOrigin.setField(base::JointState::POSITION, 0.3);
    
    //Conversion functions from C++ to Asn1 type
    asn1SccBase_JointState_toAsn1(asnVal, cppOrigin);
    
    BOOST_CHECK(asnVal.position == 0.3);
    
    //Conversion functions from asn1 to c++ type
    asn1SccBase_JointState_fromAsn1(cppDest, asnVal);



    // Test position field
    
    BOOST_CHECK(cppOrigin.hasPosition() == cppDest.hasPosition()); //true
    BOOST_CHECK(cppOrigin.hasSpeed() == cppDest.hasSpeed()); //false
    BOOST_CHECK(cppOrigin.hasEffort() == cppDest.hasEffort()); //false
    BOOST_CHECK(cppOrigin.hasRaw() == cppDest.hasRaw()); //false
    BOOST_CHECK(cppOrigin.hasAcceleration() == cppDest.hasAcceleration());//false
    BOOST_CHECK(cppOrigin.isPosition() == cppDest.isPosition()); //true
    BOOST_CHECK(cppOrigin.isSpeed() == cppDest.isSpeed()); //false
    BOOST_CHECK(cppOrigin.isEffort() == cppDest.isEffort()); //false
    BOOST_CHECK(cppOrigin.isRaw() == cppDest.isRaw()); //false
    BOOST_CHECK(cppOrigin.isAcceleration() == cppDest.isAcceleration()); //false

    BOOST_CHECK(cppOrigin.getField(base::JointState::POSITION)== cppDest.getField(base::JointState::POSITION) );
    BOOST_CHECK(cppOrigin.getMode()== cppDest.getMode());

}







