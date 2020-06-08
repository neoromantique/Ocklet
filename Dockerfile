FROM frolvlad/alpine-python3:latest


RUN apk update

RUN apk add build-base python3-dev py-pip jpeg-dev zlib-dev ffmpeg libwebp libwebp-dev
ENV LIBRARY_PATH=/lib:/usr/lib

WORKDIR /app

RUN pip3 install flask pillow

COPY . .

CMD sh /app/start.sh
