FROM python

WORKDIR /src/app

COPY requirements.txt ./

RUN pip install -r requirements.txt
