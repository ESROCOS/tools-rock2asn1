# H2020 ESROCOS Project
# Company: GMV Aerospace & Defence S.A.U.
# Licence: GPLv2

set(LIB ${"${CMAKE_PROJECT_NAME}"})

file(GLOB SOURCES RELATIVE ${"${CMAKE_CURRENT_SOURCE_DIR}"} *.cpp)

file(GLOB HEADERS RELATIVE ${"${CMAKE_CURRENT_SOURCE_DIR}"} *.h *.hpp)

set(CMAKE_CXX_FLAGS "${"${CMAKE_CXX_FLAGS}"} -DOROCOS_TARGET=gnulinux")

set(CMAKE_CXX_FLAGS "${"${CMAKE_CXX_FLAGS}"} -I ${"${CMAKE_INSTALL_PREFIX}"}/include/orocos")

# ASN.1 types are imported and compiled locally to the project, but not installed
esrocos_asn1_types_package(${"${LIB}"}_local_types
    OUTDIR asn1
    IMPORT types/${lib_name})
    
# Find libraries in ESROCOS' install directory
link_directories(${"${CMAKE_INSTALL_PREFIX}"}/lib)

# Target library
add_library(${"${LIB}"} SHARED ${"${SOURCES}"})
set_target_properties(${"${LIB}"} PROPERTIES LINKER_LANGUAGE CXX)
esrocos_pkgconfig_dependency(${"${LIB}"}
    eigen3
)
target_include_directories(${"${LIB}"} 
   PUBLIC ${"${CMAKE_INSTALL_PREFIX}"}/include
   PRIVATE ${"${CMAKE_CURRENT_BINARY_DIR}"}
)
add_dependencies(${"${LIB}"} ${"${LIB}"}_local_types_generate_c)

# Install headers, libraries and pkg-config file
install(FILES ${"${HEADERS}"}
        DESTINATION ${"${CMAKE_INSTALL_PREFIX}"}/include/${"${CMAKE_PROJECT_NAME}"}
)
        
install(TARGETS ${"${LIB}"}
        DESTINATION ${"${CMAKE_INSTALL_PREFIX}"}/lib
)

CONFIGURE_FILE("${"${LIB}"}.pc.in" "${"${LIB}"}.pc" @ONLY)
install(FILES ${"${CMAKE_CURRENT_BINARY_DIR}"}/${"${LIB}"}.pc
        DESTINATION ${"${CMAKE_INSTALL_PREFIX}"}/lib/pkgconfig
)
