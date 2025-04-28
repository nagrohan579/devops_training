FROM ubuntu

RUN apt-get update && apt-get install -y python3 python3-pip python3-flask

COPY app.py /opt/app.py

ENTRYPOINT ["flask", "--app", "/opt/app.py", "run", "--host=0.0.0.0"]