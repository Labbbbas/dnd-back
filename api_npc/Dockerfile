FROM python:3.13.0-alpine3.20

WORKDIR /app

RUN addgroup -g 1000 app && adduser -D -u 1000 -G app app

COPY --chown=app . .

# && se va a ejecutar la siguiente instrucción sólo si la anterior fue correcta
RUN apk update && \
    apk add --no-cache curl && \
    pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir gunicorn Flask flask-cors pymongo marshmallow flasgger

RUN touch /app/npc_api.log && chmod 666 /app/npc_api.log && chown app:app /app/npc_api.log

EXPOSE 8004

# || se va a ejecutar la siguiente instrucción sólo si la anterior NO fue correcta
HEALTHCHECK CMD curl --fail http://localhost:8004/healthcheck || exit 1

USER app

ENTRYPOINT [ "gunicorn", "--bind", "0.0.0.0:8004", "-w 4", "app:app" ]
