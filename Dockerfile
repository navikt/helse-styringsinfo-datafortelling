FROM python:3.11-slim-bookworm as first
WORKDIR /build

RUN apt-get update && apt-get install -yq --no-install-recommends \
    curl \
    jq \
    wget \
    locales \
    locales-all \
    python3-dev \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV LANG="en_US.utf8" \
    LANGUAGE="en_US:en"

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python -m pip install --no-cache-dir --upgrade pip wheel
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

RUN QUARTO_VERSION=$(curl https://api.github.com/repos/quarto-dev/quarto-cli/releases/latest | jq '.tag_name' | sed -e 's/[\"v]//g')  \
    && wget --quiet https://github.com/quarto-dev/quarto-cli/releases/download/v${QUARTO_VERSION}/quarto-${QUARTO_VERSION}-linux-amd64.tar.gz \
    && tar -xzf quarto-${QUARTO_VERSION}-linux-amd64.tar.gz  \
    && mv quarto-${QUARTO_VERSION} /quarto \
    && rm -rf quarto-${QUARTO_VERSION}-linux-amd64.tar.gz


FROM python:3.11-slim-bookworm
WORKDIR /app

RUN groupadd -g 1069 apprunner && \
    useradd -r -u 1069 -g apprunner apprunner

COPY --from=first /opt/venv /opt/venv
COPY --from=first /quarto /opt/quarto

RUN ln -s /opt/quarto/bin/quarto /usr/local/bin/quarto

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


RUN ipython kernel install --name "python3"

RUN apt-get update && apt-get install -yq --no-install-recommends \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY publish.sh .
COPY custom.scss .
COPY figurer/ figurer/
COPY index.qmd .

RUN chown -R apprunner:apprunner /app

USER apprunner

CMD ["./publish.sh"]
