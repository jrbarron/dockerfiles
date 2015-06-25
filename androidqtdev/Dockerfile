
FROM ahazem/android:v0.7.6

MAINTAINER Jason Barron <jason@cutehacks.com>

RUN apt-get install -y \
  build-essential \
  mesa-common-dev \
  libglu1-mesa-dev \
  subversion \
  xutils-dev \
  git \
  zip \
  vim

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
RUN svn checkout --quiet http://google-breakpad.googlecode.com/svn/trunk/@1393 google-breakpad
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
  --prefix=$SYSROOT/usr \
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
RUN wget http://www.openssl.org/source/openssl-1.0.1i.tar.gz -nv
RUN tar xzf openssl-1.0.1i.tar.gz
ENV CROSS_COMPILE arm-linux-androideabi-
WORKDIR openssl-1.0.1i
RUN ./Configure shared android-armv7 -no-ssl2 -no-ssl3 -no-comp -no-hw -no-engine --openssldir=$SYSROOT/usr
RUN make depend
RUN make all
RUN make install_sw

WORKDIR ..
RUN wget http://download.qt.io/official_releases/qt/5.4/5.4.2/single/qt-everywhere-opensource-src-5.4.2.tar.gz -nv
RUN tar xzf qt-everywhere-opensource-src-5.4.2.tar.gz
WORKDIR qt-everywhere-opensource-src-5.4.2
ENV OPENSSL_LIBS "-L$SYSROOT/usr/lib -lssl -lcrypto"
RUN ./configure \
    -v \
    -prefix /usr \
    -opensource \
    -confirm-license \
    -xplatform android-g++ \
    -sysroot $SYSROOT \
    -openssl-linked \
    -no-dbus \
    -no-strip \
    -no-widgets \
    -force-debug-info \
    -nomake tests -nomake examples -nomake tools \
    -android-sdk $ANDROID_HOME \
    -android-ndk $ANDROID_NDK_ROOT \
    -android-arch armeabi-v7a \
    -android-ndk-host linux-x86_64 \
    -android-toolchain-version 4.8 \
    -android-ndk-platform $ANDROID_API \
    -skip qttranslations -skip qtwebkit -skip qtserialport -skip qtwebkit-examples \
    -skip qtxmlpatterns -skip qtsvg -skip qtenginio -skip qtscript \
    -no-warnings-are-errors
RUN make
RUN make install

ADD symbolize.py /usr/local/bin/symbolize.py

WORKDIR $SYSROOT/usr/Qt-5.4.0
RUN symbolize.py ./lib
RUN find . -name "*.so" | xargs arm-linux-androideabi-strip

ENV PATH $PATH:/usr/Qt-5.4.0/bin

RUN rm -rf /opt/staging


