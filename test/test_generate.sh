# H2020 ESROCOS Project
# Company: GMV Aerospace & Defence S.A.U.
# Licence: GPLv2
echo "Test for ros2asn1_generate.py"
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

echo "Run ASN.1 unit tests"
./out_c/mainprogram
echo "Done."
echo ""

echo "Compile conversion functions (this may take a while)"
cd out_support/src
ln -s $AUTOPROJ_CURRENT_ROOT/tools/rock2asn1/test/out_c asn1
g++ -fPIC `pkg-config --cflags base-transport-typelib-gnulinux --cflags eigen3 --cflags base-types` -c *.cpp 
g++ -shared -o libtest_support.so *.o
if [ ! -f libtest_support.so ]; then
    echo "Build failed!"
fi
cd ../..
echo "Done."
echo ""

