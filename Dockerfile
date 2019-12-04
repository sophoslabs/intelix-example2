FROM ubuntu:18.04

ENV http_proxy=http://proxy.labs.localsite.sophos:8080
ENV https_proxy=http://proxy.labs.localsite.sophos:8080

COPY requirements.txt /

RUN apt update -y && apt upgrade -y && apt install -y \
	build-essential \
	python3-dev \
	python3-pip \
	curl \
	vim \
	&& pip3 install -r /requirements.txt \
	&& rm -rf /var/lib/apt/lists/* \
	&& apt-get purge -y --auto-remove gcc


COPY resources/entry.sh /

RUN mkdir -p /app
COPY projectq_project /app/projectq_project
WORKDIR /app/projectq_project

EXPOSE 8000
ENTRYPOINT ["/bin/bash"]
CMD ["/entry.sh"]


