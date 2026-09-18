# Docker Setup Guide

## Prerequisite
Before proceeding, follow the Prime and Spines configuration steps located in the root directory of this repository.

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

## Step 3
With the same directory open, run: 

```bash
docker compose up
```
This creates all containers and starts them and their respective processes/services (as specified in docker-compose.yml). 

## Step 4
In a separate terminal window, run: 

```bash
docker exec -it prime1 bash
```
This opens an interactive Bash shell inside the **prime1** container. 

## Step 5 
In the same window open from step 3, you can now run the driver program using:

```bash
./driver -l <local_IP> -i <client_ID> -s <server_ID> -c <update_count> -n <emulated_clients>
```
Example input:
```bash
./driver -l 172.20.0.2 -i 1 -s 1 -c 10000 -n 24
```



# Docker Teardown Guide
With a terminal window open in `cs2910/prime/docker` run:

```bash
docker compose down
```
This terminates and deletes all existing containers and the Docker network. If any changes are pushed to the GitHub and you want these to be reflected in 
a new image restart this process starting from Step 2. 

To delete the images, run:

```bash
docker rmi replica-img prime-base
```





