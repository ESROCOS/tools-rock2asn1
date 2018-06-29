# Generated from ${context._with_template.uri} for ${lib_name}.

esrocos_asn1_types_package(esrocos_types_${lib_name}
    ${lib_name}.asn        
    taste-extended.asn  
    taste-types.asn
    userdefs.asn
)

esrocos_asn1_types_build_test(esrocos_types_${lib_name})
esrocos_asn1_types_install(esrocos_types_${lib_name} ${"${CMAKE_INSTALL_PREFIX}"}/types/${lib_name})

