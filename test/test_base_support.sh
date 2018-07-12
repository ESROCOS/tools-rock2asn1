echo "Test for base_support"
echo ""

PYTHONPATH=../python:$PYTHONPATH

echo "Clear old results"
rm -rf out_asn out_c out_support
mkdir -p out_asn out_c out_support
echo "Done."
echo ""

echo "Run generation"
../python/rock2asn1_generate.py base.tlb out_asn out_support
echo "Done."
echo ""

echo "Copying modified userdefs-base.asn to execute the unit tests for base_support"
cp src_support/userdefs-base.asn out_asn/asn/


echo "Run ASN.1 compilation to C"
asn1.exe -c -o out_c -uPER --type-prefix asn1Scc -atc out_asn/asn/* 
echo "Done."
echo ""


echo "Compile C code"
cd out_c
make
cd ..
echo "Done."
echo ""


echo "Compile conversion functions (this may take a while)"
cd out_support/src
ln -s ../../out_c asn1
g++ -fPIC `pkg-config --cflags base-transport-typelib-gnulinux --cflags eigen3 --cflags base-types` -c *.cpp asn1/*.c
g++ -shared -o libtest_support.so *.o
if [ ! -f libtest_support.so ]; then
    echo "Build failed!"
fi

echo "Compile main function"
cp ../../src_support/main.cpp .

g++ -fPIC `pkg-config --cflags base-transport-typelib-gnulinux --cflags eigen3 --cflags base-types` -c main.cpp 
g++ -L. -L${AUTOPROJ_CURRENT_ROOT}/install/lib -lbase-types -ltest_support -o main main.o

if [ -f main ]; then
    echo "Executing test function"
    ./main
else
    echo "Test build  failed!"
fi
cd ../..
echo "Done."
echo ""

