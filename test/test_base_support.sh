if [ -d out_support ]; then 
    echo 'Test for base_support library'
    
    cd out_support/src

    echo "Compiling test function"
    cp ../../src_support/*.cpp .
    cp ../../src_support/*.hpp .

    #g++ -I. -fPIC `pkg-config --cflags base-transport-typelib-gnulinux --cflags eigen3 --cflags base-types` -c main.cpp test_frame.cpp
    #g++ -L. -L${AUTOPROJ_CURRENT_ROOT}/install/lib -lbase-types -ltest_support -o main main.o test_frame.o
    rm -r asn1
    mkdir asn1
    
    echo "Run ASN.1 compilation to C"
    asn1.exe -c -o asn1 -uPER --type-prefix asn1Scc -atc ../../out_asn/asn/base.asn ../../out_asn/asn/taste-types.asn ../../out_asn/asn/taste-extended.asn ../../src_support/userdefs-base.asn
    
    cd asn1
    make
    rm mainprogram.o
    cd ..

    g++ -I. -fPIC `pkg-config --cflags base-transport-typelib-gnulinux --cflags eigen3 --cflags base-types` -c test.cpp 
    
    #rm asn1/testsuite*
    #rm asn1/test_case*
    #rm asn1/acn1srct.o

    g++ -L. -L${AUTOPROJ_CURRENT_ROOT}/install/lib -lbase-types -ltest_support -lboost_system -lboost_thread -lboost_unit_test_framework -DBOOST_TEST_MAIN  -o  test test.o asn1/*.o -fprofile-arcs
   # export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$PWD

    if [ -f test ]; then
        echo "Executing test function"
        ./test
    else
        echo "Test build  failed!"
    fi
    cd ../..
    echo "Done."
    echo ""
else    
    echo "Please generate asn library and support library running ./test_generate.sh "
    echo "Test Failed."
    echo ""
fi

