FROM python:3.8.3

WORKDIR /usr/src/app

COPY entrypoint.py /

EXPOSE 80

ENTRYPOINT ["python", "/entrypoint.py"]