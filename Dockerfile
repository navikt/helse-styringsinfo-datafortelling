FROM navikt/python:3.11

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


COPY index.qmd .
COPY publish.sh .
COPY requirements.txt .

RUN python -m pip install --upgrade pip wheel
RUN python -m pip install -r requirements.txt
RUN ipython kernel install --name "python3"

CMD ["./publish.sh"]