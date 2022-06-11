FROM ubuntu:latest AS webservice
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask pymongo
EXPOSE 5000
ADD data /data
ADD src /src
ADD templates /src/templates
ADD static /src/static
ENTRYPOINT [ "python3", "-u", "/src/service.py" ]