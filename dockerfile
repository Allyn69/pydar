FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
&& apt-get install -y python3-pip python3-dev \
&& cd /usr/local/bin \
&& ln -s /usr/bin/python3 python \
&& pip3 install --upgrade pip

RUN apt-get install -y libproj-dev proj-data proj-bin \
&& apt-get install -y libgeos-dev python3-tk

ADD requirements.txt /

RUN pip install -r requirements.txt

ADD airport.py /

ENTRYPOINT ["python3", "airport.py"]
