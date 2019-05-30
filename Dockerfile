FROM debian:latest
COPY . /app
RUN apt-get update 
RUN apt-get upgrade
RUN apt-get -y install python3 python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install -r /app/requirements.txt
# RUN python3 /app/populate_database.py /app/data/
EXPOSE 5000
CMD python3 /app/app.py
