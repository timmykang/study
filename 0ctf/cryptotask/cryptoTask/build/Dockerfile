FROM ubuntu:xenial

MAINTAINER 0ops

ENV LC_ALL C
ENV LD_LIBRARY_PATH /usr/local/lib/

RUN apt-get update \
    && apt-get install -y libboost-all-dev libmysql++-dev mysql-client 

RUN useradd -m ctf

COPY ./bin/cryptoTask //home/ctf
COPY ./bin/wait-for-it.sh /home/ctf

RUN chmod +x /home/ctf/cryptoTask
RUN chmod +x /home/ctf/wait-for-it.sh

WORKDIR /home/ctf

USER ctf

CMD /home/ctf/wait-for-it.sh mysql:3306 -- /home/ctf/cryptoTask 
#CMD /home/ctf/wait-for-it.sh mysql:3306 -- sleep infinity
