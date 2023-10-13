FROM ghcr.io/navikt/baseimages/python:3.11

USER root


RUN apt-get update && apt-get install -yq --no-install-recommends \
    curl \
    jq \
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*


RUN QUARTO_VERSION=$(curl https://api.github.com/repos/quarto-dev/quarto-cli/releases/latest | jq '.tag_name' | sed -e 's/[\"v]//g') && \
    wget https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.tar.gz && \
    tar -xvzf quarto-${QUARTO_VERSION}-linux-amd64.tar.gz && \
    ln -s /app/quarto-${QUARTO_VERSION}/bin/quarto /usr/local/bin/quarto && \
    rm -rf quarto-${QUARTO_VERSION}-linux-amd64.tar.gz

RUN groupadd -g 1069 python && \
    useradd -r -u 1069 -g python python

WORKDIR /home/python

COPY . .
RUN python -m pip install --upgrade pip wheel
RUN python -m pip install .
RUN ipython kernel install --name "python3"

RUN chown python:python /home/python -R
USER python

CMD ["./publish.sh"]
