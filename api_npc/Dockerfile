FROM python:3.13.0-alpine3.20

WORKDIR /app

RUN addgroup -g 1000 app && adduser -D -u 1000 -G app app

COPY --chown=app . .

RUN chmod 777 /app

RUN apk update && \
    apk add --no-cache curl && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir gunicorn Flask flask-cors pymongo marshmallow flasgger

EXPOSE 8004

HEALTHCHECK CMD curl --fail http://$(ip -o -4 addr list | grep eth0 | awk '{print $4}' | sed 's/...$//'):8004/healthcheck || exit 1

USER app

ENTRYPOINT ["gunicorn", "--bind", "0.0.0.0:8004", "-w 4", "app:app"]