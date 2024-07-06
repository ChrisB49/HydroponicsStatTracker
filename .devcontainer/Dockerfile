# First stage: Build Python 3.11 from source on Debian 11
FROM debian:bookworm as debian_base

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y wget build-essential libncursesw5-dev libssl-dev \
    libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev \
    python3-pip python3-dev git python-is-python3 locales sed
RUN sed -i 's/^# *\(en_US.UTF-8\)/\1/' /etc/locale.gen && locale-gen