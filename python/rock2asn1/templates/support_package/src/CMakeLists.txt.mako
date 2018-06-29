# Generated from ${context._with_template.uri} for ${lib_name}.

set(LIB ${"${CMAKE_PROJECT_NAME}"})

file(GLOB SOURCES RELATIVE ${"${CMAKE_CURRENT_SOURCE_DIR}"} *.cpp)
file(GLOB HEADERS RELATIVE ${"${CMAKE_CURRENT_SOURCE_DIR}"} *.h *.hpp)


# ASN.1 types are imported and compiled locally to the project, but not installed
esrocos_asn1_types_package(${"${LIB}"}_local_types
    OUTDIR asn1
    IMPORT types/${lib_name})
    
# Find libraries in ESROCOS' install directory
if(${"${CMAKE_CROSSCOMPILING}"})
    link_directories(${"${CMAKE_INSTALL_PREFIX}"}/${"${RCC_TARGET}"}/lib)
else()
    link_directories(${"${CMAKE_INSTALL_PREFIX}"}/lib)
endif()

# Target library
if(${"${CMAKE_CROSSCOMPILING}"})
    # Compiling for RTEMS, build static library
    add_library(${"${LIB}"} STATIC ${"${SOURCES}"})
else()
    # Compiling natively, build shared library	
    add_library(${"${LIB}"} SHARED ${"${SOURCES}"})
endif()

set_target_properties(${"${LIB}"} PROPERTIES LINKER_LANGUAGE CXX)
esrocos_pkgconfig_dependency(${"${LIB}"}
    eigen3
)
target_include_directories(${"${LIB}"} 
   PUBLIC ${"${CMAKE_INSTALL_PREFIX}"}/include
   PUBLIC ${"${CMAKE_INSTALL_PREFIX}"}/include/orocos
   PRIVATE ${"${CMAKE_CURRENT_BINARY_DIR}"}
)
target_compile_definitions(${"${LIB}"} PUBLIC OROCOS_TARGET=${"$"}ENV{OROCOS_TARGET})
add_dependencies(${"${LIB}"} ${"${LIB}"}_local_types_generate_c)

# Install headers, libraries and pkg-config file
install(FILES ${"${HEADERS}"}
        DESTINATION ${"${CMAKE_INSTALL_PREFIX}"}/include/${"${CMAKE_PROJECT_NAME}"}
)

if(CMAKE_CROSSCOMPILING) 
    install(TARGETS ${"${LIB}"} DESTINATION ${"${CMAKE_INSTALL_PREFIX}"}/${"${RCC_TARGET}"}/lib)
else()
    install(TARGETS ${"${LIB}"} DESTINATION ${"${CMAKE_INSTALL_PREFIX}"}/lib)
endif()

if(CMAKE_CROSSCOMPILING)
    CONFIGURE_FILE("${"${LIB}"}.pc.in" "${"${LIB}"}.pc" @ONLY)
    install(FILES ${"${CMAKE_CURRENT_BINARY_DIR}"}/${"${LIB}"}.pc
        DESTINATION ${"${CMAKE_INSTALL_PREFIX}"}/${"${RCC_TARGET}"}/lib/pkgconfig
    )
else()
    CONFIGURE_FILE("${"${LIB}"}.pc.in" "${"${LIB}"}.pc" @ONLY)
    install(FILES ${"${CMAKE_CURRENT_BINARY_DIR}"}/${"${LIB}"}.pc
        DESTINATION ${"${CMAKE_INSTALL_PREFIX}"}/lib/pkgconfig
    )
endif()

