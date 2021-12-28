# start by pulling the python image
FROM python:3.8-alpine

LABEL maintainer="Koteswara Singamsetty"

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN apk update
RUN apk add make automake gcc g++ subversion python3-dev
#RUN pip install pandas Flask
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD ["hdb_ml_server.py" ]