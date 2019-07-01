FROM ubuntu
RUN apt-get update
RUN apt-get install -y build-essential \
		 curl \
		python3-pip \
		swig
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install --assume-yes apt-utils
RUN apt-get update \
	&& apt-get install -y apt-transport-https ca-certificates gnupg software-properties-common wget \
        && wget -O - https://apt.kitware.com/keys/kitware-archive-latest.asc 2>/dev/null | apt-key add - \	
	&& apt-add-repository 'deb https://apt.kitware.com/ubuntu/ bionic main' \
	&& apt-get update	\
	&& apt-get install -y kitware-archive-keyring \
	&& apt-key --keyring /etc/apt/trusted.gpg del C1F34CDD40CD72DA \ 
	&& apt-get install -y cmake \
	&& apt-get install -y make \
	&& apt-get install -y git
RUN rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip
RUN pip3 install jupyter -U

WORKDIR /src


EXPOSE 8888

ENTRYPOINT ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root"]

ADD . /src

RUN pip3 install -r requirments.txt
