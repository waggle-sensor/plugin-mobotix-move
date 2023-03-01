# Running docker image
FROM waggle/plugin-base:1.1.1-base

COPY requirements.txt /app/
RUN apt-get -y update; apt-get -y install curl
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

COPY app /app/

#ENTRYPOINT ["python3", "/app/app.py"]
