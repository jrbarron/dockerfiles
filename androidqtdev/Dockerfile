
FROM ahazem/android:v0.7.6

MAINTAINER Jason Barron <jason@cutehacks.com>

ENV ANDROID_NDK_ROOT /usr/local/android-ndk

RUN apt-get install -y build-essential mesa-common-dev libglu1-mesa-dev

# Download and build Qt
RUN wget http://download.qt-project.org/official_releases/qt/5.3/5.3.2/single/qt-everywhere-opensource-src-5.3.2.tar.gz
RUN tar xzvf qt-everywhere-opensource-src-5.3.2.tar.gz
WORKDIR qt-everywhere-opensource-src-5.3.2
RUN ./configure \
    -v \
    -opensource \
    -confirm-license \
    -xplatform android-g++ \
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
