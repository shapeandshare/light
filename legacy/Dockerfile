FROM ubuntu

RUN apt-get update
RUN apt-get upgrade -y

# libtinfo5
RUN apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev cmake libffi-dev libssl-dev

RUN python3 -m venv venv
RUN source venv/bin/activate
RUN pip3 install --upgrade Cython==0.29.33 virtualenv  # the --user should be removed if you do this in a venv

# add the following line at the end of your ~/.bashrc file
RUN export PATH=$PATH:~/.local/bin/

COPY . /opt/tiland/
WORKDIR /opt/tiland/
