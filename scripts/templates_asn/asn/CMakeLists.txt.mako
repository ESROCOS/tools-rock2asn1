# H2020 ESROCOS Project
# Company: GMV Aerospace & Defence S.A.U.
# Licence: GPLv2



esrocos_asn1_types_package(esrocos_types_${lib_name}
        ${lib_name}.asn        
        taste-extended.asn  
        taste-types.asn
        userdefs.asn
        )

esrocos_asn1_types_build_test(esrocos_types_${lib_name})
esrocos_asn1_types_install(esrocos_types_${lib_name} ${"${CMAKE_INSTALL_PREFIX}"}/types/${lib_name})

