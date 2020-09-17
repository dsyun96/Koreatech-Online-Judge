FROM ubuntu:18.04

RUN apt update
RUN apt install -y python3.7 python3-pip
RUN apt install -y libseccomp-dev
RUN apt install -y gcc cmake git
RUN apt install -y openjdk-8-jdk

RUN git clone https://github.com/QingdaoU/Judger.git
WORKDIR /Judger/
RUN mkdir build && cd build && cmake .. && make && make install
WORKDIR /Judger/bindings/Python/
RUN python3 setup.py install

COPY requirements.txt /Koreatech-OJ/
WORKDIR /Koreatech-OJ/
RUN pip3 install -r requirements.txt

WORKDIR /Koreatech-OJ/
COPY . .

