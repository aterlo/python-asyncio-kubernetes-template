FROM fedora
MAINTAINER Dan Siemon <dan@aterlo.com>
RUN dnf -y --refresh update
RUN dnf -y install dnf-plugins-core
RUN dnf copr enable -y mstuchli/Python3.5
RUN dnf install -y python35-python3

# Add a user to run our service. Running as root even in a container is a bad idea.
RUN /usr/sbin/useradd run

RUN mkdir /build
COPY requirements.txt /build/
COPY simple-server.py /build/
RUN pip3.5 install -U -r /build/requirements.txt
CMD su run -c "python3.5 /build/simple-server.py"
