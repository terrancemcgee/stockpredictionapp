FROM python:3.7
WORKDIR /tmp
RUN pip install numpy
RUN pip install pandas
RUN pip install sqlalchemy
# TA-Lib
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
 tar -xvzf ta-lib-0.4.0-src.tar.gz && \
 cd ta-lib/ && \
 ./configure — prefix=/usr && \
 make && \
 make install && \
 cd .. && \
 wget https://files.pythonhosted.org/packages/90/05/d4c6a778d7a7de0be366bc4a850b4ffaeac2abad927f95fa8ba6f355a082/TA-Lib-0.4.17.tar.gz && \
 tar xvf TA-Lib-0.4.17.tar.gz && \
 cd TA-Lib-0.4.17 && \
 python setup.py install && \
 cd ..
RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz TA-Lib-0.4.17 TA-Lib-0.4.17.tar.gz
