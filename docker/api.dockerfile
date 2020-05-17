FROM python:3.6

ENV PROJECT_ROOT /home/iqvizyon

COPY ./requirements.txt $PROJECT_ROOT/
RUN pip install -r $PROJECT_ROOT/requirements.txt

ADD ./src $PROJECT_ROOT/src/

ENV PYTHONPATH $PROJECT_ROOT/
ENV PYTHONPATH $PROJECT_ROOT/src
ENV KANBAN_ENV_FILE $PROJECT_ROOT/.env

WORKDIR $PROJECT_ROOT

EXPOSE 8081