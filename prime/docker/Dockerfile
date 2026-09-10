# Using ubuntu 22.04 [replace with almalinux:9 if any issues]
FROM ubuntu:22.04

# Install dependencies [note: flex, bison, byacc required for spines parser]
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    make \
    libssl-dev \
    flex \
    bison \
    git
        # byacc \

# Clone the CS2910 repository [in the root directory]
WORKDIR /root
RUN git clone https://github.com/sam444555/cs2910.git

# Configure and compile spines
WORKDIR /root/cs2910/prime/spines
RUN chmod +x configure
RUN ./configure
RUN make -C daemon parser
RUN make

# Compile prime 
WORKDIR /root/cs2910/prime/src
RUN make



