FROM ubuntu
RUN apt-get update
RUN apt-get install -y build-essential \
		 curl \
		python3-pip \
		swig 
RUN rm -rf /var/lib/apt/lists/*
RUN pip3 install --upgrade pip
RUN pip3 install jupyter -U

WORKDIR /src


EXPOSE 8888

ENTRYPOINT ["jupyter", "notebook", "--ip=0.0.0.0", "--allow-root"]

ADD . /src

RUN pip3 install -r requirments.txt
