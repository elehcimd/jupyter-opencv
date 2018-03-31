FROM ubuntu:16.04
MAINTAINER Michele Dallachiesa <michele.dallachiesa@gmail.com>
# Container providing Jupyter notebook server with Python3 bindings for OpenCV 3.4.0
# Based on https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/
# Not compiling/installing templates, added gtk support

USER root

# Update package list, upgrade system and set default locale
RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get -y install apt-utils
RUN apt-get -y install locales
RUN locale-gen "en_US.UTF-8"
RUN dpkg-reconfigure --frontend=noninteractive locales
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8

# Install python3, and activate python3.5 as default python interpreter
RUN apt-get -y install python3-dev python3 python3-pip python3-venv
RUN pip3 install --upgrade pip
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.5 1

# Install packages required for compiling opencv
RUN apt-get -y install build-essential cmake pkg-config wget

# Install packages providing support for several image formats
RUN apt-get -y install libjpeg8-dev libtiff5-dev libjasper-dev libpng12-dev

# Install packages providing support for several video formats
RUN apt-get -y install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev

# Install gtk (GUI components in opencv rely on gtk)
RUN apt-get -y install libgtk-3-dev

# Install additional packages optimizing opencv
RUN apt-get -y install libatlas-base-dev gfortran

# Define OpenCV version to download, compile and install
ENV OPENCV_VERSION 3.4.0

WORKDIR /root
RUN wget -O opencv.tgz https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.tar.gz
RUN wget -O opencv_contrib.tgz https://github.com/Itseez/opencv_contrib/archive/${OPENCV_VERSION}.tar.gz
RUN tar xzf opencv.tgz
RUN tar xzf opencv_contrib.tgz
RUN mkdir /root/opencv-${OPENCV_VERSION}/build

# numpy required for OpenCV Python bindings
RUN pip3 install numpy==1.14.2

# Configure
RUN cd /root/opencv-${OPENCV_VERSION}/build && \
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-${OPENCV_VERSION}/modules \
        -D PYTHON_EXECUTABLE=/usr/bin/python \
        -D BUILD_EXAMPLES=OFF \
        -D BUILD_DOCS=OFF \
        -D BUILD_PERF_TESTS=OFF \
        -D BUILD_TESTS=OFF \
        ..

# Compile
RUN cd /root/opencv-${OPENCV_VERSION}/build && make

# Install
RUN cd /root/opencv-${OPENCV_VERSION}/build && make install
RUN ldconfig

# Remove source code and temporary files
RUN rm -rf /root/opencv*

# OpenCV installation completed!

# Install python packages for data science
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Install additional system packages
RUN apt-get -y install x11-apps

# Create/populate /playground directory and define entrypoint
RUN mkdir /playground
COPY datasets /playground/datasets
COPY lab /playground/lab
COPY notebooks /playground/notebooks
RUN echo >/playground/WARNING:\ Any\ modification\ might\ be\ lost\ at\ container\ termination\!

ENV PYTHONPATH /playground
WORKDIR /playground
CMD ["jupyter", "notebook", "--allow-root", "--ip=0.0.0.0", "--NotebookApp.token=", "/playground"]

EXPOSE 8888/tcp

