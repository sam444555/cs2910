#NOTES:
#   This is running on Docker for Windows and may experience issues in other OS environments
#   Todo:
#       >add macOS version
#       >add keygen optimizations
#
#   Building the image: docker build -t replica-image .
#   Building the image fresh: docker build --no-cache -t replica-image .

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
    git \
    groff \
    python3
    # groff required for libspread-util manual pages during compiliation, fixes E_get_time.0 issue
    # if python doesn't work use python3

# Clone the CS2910 repository [in the root directory]
WORKDIR /root
RUN git clone https://github.com/sam444555/cs2910.git

# Configure and compile spines
WORKDIR /root/cs2910/prime/spines
# Make the scripts used executable [Windows/Linux executable permission compatibility issue]
RUN chmod +x configure && \
    chmod +x stdutil/configure && \
    chmod -R +x stdutil/buildtools && \
    chmod +x libspread-util/configure && \
    chmod -R +x libspread-util/buildtools
RUN ./configure
RUN make -C daemon parser
RUN make

# generate spines keys
WORKDIR /root/cs2910/prime/spines/daemon
RUN chmod +x gen_keys.sh && ./gen_keys.sh

# Compile prime
WORKDIR /root/cs2910/prime
# Make the scripts used executable [Windows/Linux executable permission compatibility issue]
RUN chmod +x stdutil/configure && \
    chmod -R +x stdutil/buildtools && \
    chmod +x libspread-util/configure && \
    chmod -R +x libspread-util/buildtools && \
    chmod +x OpenTC-1.1/TC-lib-1.0/configure && \
    chmod +x OpenTC-1.1/TC-lib-1.0/missing

WORKDIR /root/cs2910/prime/src
RUN make

# generate prime keys
WORKDIR /root/cs2910/prime/bin
RUN ./gen_keys



