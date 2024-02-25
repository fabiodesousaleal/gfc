FROM ubuntu:latest

WORKDIR /app

COPY requirements.txt .

RUN apt update -y && apt install -y python3.11 \
python3.11-venv \
python3-pip \
python3.11 -m venv /venv 

ENV PATH="/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt
RUN echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections
RUN echo "ttf-mscorefonts-installer msttcorefonts/present-mscorefonts-eula note" | debconf-set-selections
RUN apt-get install -y ttf-mscorefonts-installer \
poppler-utils
EXPOSE 5000

CMD ["bash", "-c", "source /venv/bin/activate && python3.11 app.py"]
