FROM python:3.13.5
#RUN echo "hello mani!!!!" > /usr/share/nginx/html/index.html
WORKDIR /
COPY ./req.txt ./req.txt
RUN pip3 install -r req.txt
ENV MY_MYSQL_USER=''
ENV MY_DATABASE_NAME=''
ENV MY_MYSQL_HOST=''
ENV MY_MYSQL_PASSWORD=''
ENV AWS_ACCESS_KEY=''
ENV AWS_SECRET_ACCESS_KEY=''
RUN apt-get update && apt install -y curl supervisor nginx
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY ./src.py ./src.py
COPY ./s3.py ./s3.py
COPY ./nginx.conf /etc/nginx/sites-available/default
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./s3.conf /etc/supervisor/conf.d/s3.conf
COPY ./animeapi.conf /etc/supervisor/conf.d/animeapi.conf

ENTRYPOINT ["/usr/bin/supervisord"]