FROM python

WORKDIR /app
COPY . /app
RUN python setup.py install
CMD bash
