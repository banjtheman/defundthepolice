FROM python:3.8-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=true
RUN apt-get  update &&  apt-get install -y build-essential
ADD requirements/api.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt --no-cache-dir
RUN  apt-get remove -y gcc build-essential&& apt-get autoremove -y && apt-get clean -y
