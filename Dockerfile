FROM python:3.9
RUN apt update && apt install -y wget
RUN wget https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64 -O /usr/bin/yq &&\
    chmod +x /usr/bin/yq
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN git config --global --add safe.directory /app
RUN rm -rf .git
RUN rm -rf metrics
RUN chmod +x ./scripts/*
ENTRYPOINT ["./scripts/entrypoint.sh"]
