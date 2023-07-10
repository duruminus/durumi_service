FROM pytorch/pytorch

WORKDIR /app

COPY . .


RUN apt-get update
RUN apt-get -y install libgl1-mesa-glx
RUN apt-get -y install libglib2.0-0
# RUN pip3 install cmake
RUN pip3 install -r requirements.txt

EXPOSE 80

CMD python3 app.py



