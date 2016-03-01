#!/bin/bash
set -e
PREFIX=/usr/lib
if [ "$1" != "" ]; then
    PREFIX="$1"
fi
cd libseccomp
./autogen.sh
./configure --prefix=$PREFIX
make
make install
cd src/python
cython -3 seccomp.pyx
gcc -fPIC -shared $(pkg-config --cflags python3) seccomp.c -o seccomp.so -lseccomp
mkdir -p /opt/harnas-tools
install --mode 0755 seccomp.so /opt/harnas-tools/seccomp.so
cd ../../..
for name in harnas-compile harnas-run harnas-diff harnas-check harnas-sandbox; do
    install --mode 0755 $name /opt/harnas-tools/$name
    ln -sf /opt/harnas-tools/$name /usr/bin/$name
done
