# base image  
FROM python:3.8   
# setup environment variable  
ENV DockerHOME=/home/app/webapp  

# set work directory  
RUN mkdir -p $DockerHOME  

# where your code lives  
WORKDIR $DockerHOME  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  
# install dependencies  
RUN pip install --upgrade pip  
# copy whole project to your docker home directory. 
COPY . $DockerHOME  
# run this command to install all dependencies  
RUN pip install -r requirements.txt  

RUN python3 -m nltk.downloader averaged_perceptron_tagger
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader wordnet
RUN python3 -m spacy download fr_core_news_sm
RUN python3 -m nltk.downloader words
RUN python3 -m nltk.downloader stopwords
RUN python3 -m nltk.downloader maxent_ne_chunker
# port where the Django app runs  
EXPOSE 8000  
# start server  
RUN python manage.py makemigrations
RUN python manage.py migrate
CMD python manage.py runserver  
