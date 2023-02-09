# Social Network API App

## Docker Compose for postgres

```
version: '3.9'
services:
  postgres:
    image: postgres:14.1-alpine
    restart: always
    environment:
      - POSTGRES_USER=<your user>
      - POSTGRES_PASSWORD=<your password>
    ports:
      - '5432:5432'
    volumes:
      - <your volume>:/var/lib/postgresql/data
volumes:
  postgres:
    driver: local
```
