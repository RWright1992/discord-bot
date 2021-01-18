FROM python:3.6
WORKDIR /opt
COPY . /opt
RUN pip3 install -U -r requirements.txt
RUN apt-get update && apt install -y ffmpeg
ENTRYPOINT [ "/usr/local/bin/python3", "bennys-bot.py" ]