
FROM ahazem/android:v0.7.6

MAINTAINER Jason Barron <jason@cutehacks.com>

RUN apt-get install -y \
  build-essential \
  mesa-common-dev \
  libglu1-mesa-dev \
  subversion \
  xutils-dev

# Build everything here
WORKDIR /opt
RUN mkdir staging
WORKDIR staging

ENV ANDROID_NDK_ROOT /usr/local/android-ndk
ENV ANDROID_SDK_ROOT $ANDROID_HOME
ENV ANDROID_EABI arm-linux-androideabi-4.8
ENV ANDROID_ARCH arch-arm
ENV ANDROID_API android-19
ENV ANDROID_API_VERSION $ANDROID_API
ENV PATH $PATH:$ANDROID_NDK_ROOT/toolchains/$ANDROID_EABI/prebuilt/linux-x86_64/bin
ENV SYSROOT $ANDROID_NDK_ROOT/platforms/$ANDROID_API/$ANDROID_ARCH
ENV ANDROID_DEV $SYSROOT/usr

# Download google-breakpad
RUN svn checkout http://google-breakpad.googlecode.com/svn/trunk/ google-breakpad
RUN mkdir google-breakpad-host
RUN mkdir google-breakpad-target

# Build host tools
WORKDIR google-breakpad-host
RUN ../google-breakpad/configure
RUN make
RUN make install

# Build target library for Android
WORKDIR ../google-breakpad-target
RUN ../google-breakpad/configure --host=arm-linux-androideabi \
  --prefix=/opt \
  --disable-processor \
  --disable-tools \
  CC="arm-linux-androideabi-gcc --sysroot=$SYSROOT" \
  CXX="arm-linux-androideabi-g++ --sysroot=$SYSROOT" \
  CPPFLAGS="-I$ANDROID_NDK_ROOT/sources/cxx-stl/gnu-libstdc++/4.8/include -I$ANDROID_NDK_ROOT/sources/cxx-stl/gnu-libstdc++/4.8/libs/armeabi-v7a/include" \
  LDFLAGS="-L$ANDROID_NDK_ROOT/sources/cxx-stl/gnu-libstdc++/4.8/libs/armeabi-v7a -L$SYSROOT/usr/lib" \
  LIBS="-lgnustl_shared -llog -lz -lm -ldl -lc -lgcc"
RUN make
RUN make install

# Download and build OpenSSL for Android
WORKDIR ..
RUN wget http://www.openssl.org/source/openssl-1.0.1i.tar.gz
RUN tar xzvf openssl-1.0.1i.tar.gz
ENV CROSS_COMPILE arm-linux-androideabi-
WORKDIR openssl-1.0.1i
RUN ./Configure shared android-armv7 -no-ssl2 -no-ssl3 -no-comp -no-hw -no-engine --openssldir=/opt
RUN make depend
RUN make all
RUN make install_sw

# Download and build Qt
WORKDIR ..
RUN wget http://download.qt-project.org/official_releases/qt/5.3/5.3.2/single/qt-everywhere-opensource-src-5.3.2.tar.gz
RUN tar xzvf qt-everywhere-opensource-src-5.3.2.tar.gz
WORKDIR qt-everywhere-opensource-src-5.3.2
ENV OPENSSL_LIBS "-L/opt/lib -lssl -lcrypto"
RUN ./configure \
    -v \
    -opensource \
    -confirm-license \
    -xplatform android-g++ \
    -sysroot $SYSROOT \
    -openssl-linked \
    -no-strip \
    -force-debug-info \
    -nomake tests -nomake examples \
    -android-sdk $ANDROID_HOME \
    -android-ndk $ANDROID_NDK_ROOT \
    -android-arch armeabi-v7a \
    -android-ndk-host linux-x86_64 \
    -android-toolchain-version 4.8 \
    -android-ndk-platform 19 \
    -skip qttranslations -skip qtwebkit -skip qtserialport -skip qtwebkit-examples \
    -no-warnings-are-errors
RUN make

# TODO: generate symbol files for Qt

# TODO: Run strip on the binaries
