FROM python:3

# set a directory for the app
WORKDIR /usr/src/app

# copy all the files to the container
COPY . .

# install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN python manage.py makemigrations survey
RUN python manage.py migrate 
RUN python manage.py collectstatic --noinput
 


CMD gunicorn project.wsgi:application --bind 0.0.0.0:$PORT
