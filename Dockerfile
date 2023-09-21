### Build Prism and Prism Games
FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive 

# Update and install necessary tools (vim is just an option)
RUN apt-get -y update
RUN apt -y install make gcc g++ git wget vim
# RUN apt -y install python
RUN apt -y install python3-pip build-essential

# Install Default JAVA for building prism
RUN apt -y install default-jdk
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
# Install JAVA8 for building PPL
RUN apt -y install openjdk-8-jdk libgmp-dev m4
ENV JAVA8_HOME=/usr/lib/jvm/java-8-openjdk-amd64

# Build PPL Library with the option of java (for enabling java interface)
RUN wget http://www.bugseng.com/products/ppl/download/ftp/releases/1.2/ppl-1.2.tar.gz \
    && tar xfz ppl-1.2.tar.gz \
    && cd ppl-1.2 \
    && ./configure --enable-interfaces=java --with-java=$JAVA8_HOME \
    && make -j 4 \
    && make -j 4 install

# Build prism-games
RUN git clone https://github.com/prismmodelchecker/prism-games.git \
    && cd prism-games/prism \
    && make -j 4 PPL_DIR=/usr/local/lib


# Build Andrew's Modified PRISM-games
RUN  git clone https://github.com/andrewmw94/prism-games.git andrew-prism-games \
    && cd andrew-prism-games/prism \
    && git checkout d5e2d0608699d2aba01fae29f664adcdcaf0cc30 \
    && make -j 4 PPL_DIR=/usr/local/lib


# Build My Modified PRISM-games - Up to Date with PRISM Game - 09/12/23
RUN  git clone https://github.com/MuvvalaKaran/prism-games-experimental.git karan-prism-games \
    && cd karan-prism-games/prism \
    && git checkout feature/explicit_smg_loading \
    && make -j 4 PPL_DIR=/usr/local/lib


# Add PRISM Benchmarks to the docker file
RUN git clone https://github.com/prismmodelchecker/prism-benchmarks.git

# Build prism
RUN git clone https://github.com/prismmodelchecker/prism.git \
    && cd prism/prism \
    && make -j 4

# Link binary to local binaries so that we can call them from anywhere
RUN ln -s /prism-games/prism/bin/prism /usr/local/bin/prismgames
RUN ln -s /prism-games/prism/bin/xprism /usr/local/bin/xprismgames
RUN ln -s /prism/prism/bin/prism /usr/local/bin/prism
RUN ln -s /prism/prism/bin/xprism /usr/local/bin/xprism

# Build Python model to construct PRISM SG abstraction
RUN git clone https://github.com/andrewmw94/stochastic_games_for_robotics_code.git

WORKDIR /stochastic_games_for_robotics_code

RUN pip3 install numpy matplotlib pandas

RUN apt -y install pypy3

ADD ../ ./

ENTRYPOINT "/bin/bash"