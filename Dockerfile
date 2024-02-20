# syntax=docker/dockerfile:1
FROM python:3.8-alpine

FROM ubuntu

COPY . ./
RUN chmod 1777 /tmp
# need git to install dependencies
RUN apt-get upgrade -y 
RUN apt-get update -y
RUN apt-get install -y python3-pip

# intallation of lxml requires 
RUN STATIC_DEPS=true pip3 install lxml
RUN pip3 install -r ./requirements.txt

CMD python3 ./main.py -l=DEBUG -d=/toolshed/logs/summary.log