FROM ubuntu

RUN apt-get update && apt-get install nginx supervisor python-pip git curl -y

RUN pip install --upgrade pip && pip install bottle && git clone https://github.com/HewlettPackard/python-hpOneView.git && cd python-hpOneView && pip install .

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY frontend/dist/ /var/www/html
COPY backend/backend.py /

CMD ["/usr/bin/supervisord"]

EXPOSE 80
