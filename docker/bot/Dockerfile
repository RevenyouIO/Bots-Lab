FROM python:3.8

# Don't buffer output for Python commands
ENV PYTHONUNBUFFERED=1

# Install ta-lib from source
ENV TALIB_URL=https://netix.dl.sourceforge.net/project/ta-lib/ta-lib/0.4.0/ta-lib-0.4.0-src.tar.gz \
    TALIB_SHA1SUM=b326b91e79ca1e569e95aad91e87a38640dd5f1b

RUN curl -s -o /tmp/ta-lib.tar.gz "$TALIB_URL" \
 && echo "${TALIB_SHA1SUM}  /tmp/ta-lib.tar.gz" | sha1sum -c - \
 && cd /tmp \
 && tar xvfz ta-lib.tar.gz \
 && cd /tmp/ta-lib \
 && ./configure \
 && make \
 && make install \
 && cd /tmp \
 && rm -rf /tmp/ta-lib*

# Set up SuperCronic to schedule bot runs at predefined intervals (using supercronic.conf, see below)
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.1.9/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=5ddf8ea26b56d4a7ff6faecdd8966610d5cb9d85

RUN curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" "/usr/local/bin/${SUPERCRONIC}" \
 && ln -s "/usr/local/bin/${SUPERCRONIC}" /usr/local/bin/supercronic

WORKDIR /opt/bots

# Install Python requirements
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy project files to container
COPY . .

# Copy SuperCronic configuration file into place
COPY docker/bot/supercronic.conf supercronic.conf

# Run in test mode by default. Can be overridden from command line or docker-compose file to run in production mode.
CMD python3 run_test.py
