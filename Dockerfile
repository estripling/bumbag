FROM python:3.8-slim

# configurations
ARG USER_NAME=developer \
    USER_UID=1001 \
    CODE_DIR=/code

ENV LANG=C.UTF-8 \
    PYTHONUNBUFFERED=on \
    PYTHONFAULTHANDLER=on \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=on \
    # pip:
    PIP_NO_CACHE_DIR=on \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry:
    POETRY_VERSION=1.3.1 \
    POETRY_NO_ANSI=on \
    POETRY_NO_INTERACTION=on \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_HOME="/opt/poetry"

# shell settings
SHELL [ "/bin/bash", "-eo", "pipefail", "-c" ]

# install system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
    ca-certificates \
    bash \
    build-essential \
    curl \
    git \
    # Installing `poetry` package manager:
    # https://github.com/python-poetry/poetry
    && curl -sSL 'https://install.python-poetry.org' | python - \
    # Cleaning cache:
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="${POETRY_HOME}/bin:${PATH}"

# let scripts know we're running in Docker (useful for containerised development)
ENV RUNNING_IN_DOCKER true

# use the unprivileged user for safety
RUN useradd \
    # create a system account
    -r \
    # create the user's home directory
    -m \
    # login shell of the new account
    -s /bin/bash \
    # name of the primary group
    -g root \
    # list of supplementary groups
    -G sudo \
    # specify user
    -u ${USER_UID} ${USER_NAME}

WORKDIR ${CODE_DIR}

# install project dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root

# install project in editable mode
COPY . .
RUN poetry install

USER ${USER_NAME}
