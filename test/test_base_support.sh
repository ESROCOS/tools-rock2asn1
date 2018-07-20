if [ -d out_support ]; then 
    
    cd out_support/src

    echo "Compiling test function"
    cp ../../src_support/*.cpp .
    cp ../../src_support/*.hpp .

    #g++ -I. -fPIC `pkg-config --cflags base-transport-typelib-gnulinux --cflags eigen3 --cflags base-types` -c main.cpp test_frame.cpp
    #g++ -L. -L${AUTOPROJ_CURRENT_ROOT}/install/lib -lbase-types -ltest_support -o main main.o test_frame.o

    g++ -I. -fPIC `pkg-config --cflags base-transport-typelib-gnulinux --cflags eigen3 --cflags base-types` -c test.cpp
    g++ -L. -L${AUTOPROJ_CURRENT_ROOT}/install/lib -lbase-types -ltest_support -lboost_system -lboost_thread -lboost_unit_test_framework -o test test.o

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

