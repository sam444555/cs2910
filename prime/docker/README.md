# Docker Setup Guide

## Step 1
With a terminal window open in `cs2910/prime/docker` run:

```bash
docker build -f Dockerfile.base -t prime-base .
```
This builds the base image which consists of the OS and dependencies. <ins>**This should only be run once unless you want to change the OS or add/remove dependencies.**</ins>

## Step 2
In the same directory with terminal open, run: 

```bash
docker build --no-cache -t replica-img .
```
This builds another image on top of prime-base which clones the most up to date version of this repository and then sets up Prime/Spines. 
