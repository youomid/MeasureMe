FROM python:2-onbuild

COPY start_server.sh /start_server.sh

EXPOSE 8000

CMD ["apt-get install libxml2-dev libxslt1-dev python-dev"]

CMD ["/start_server.sh"]
