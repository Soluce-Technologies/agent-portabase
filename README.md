<p align="center">
  <img src="" alt="Portabase Agent">
</p>

<p align="center">
<a href="https://www.python.org/downloads/release/python-3120/" target="_blank">
    <img src="https://img.shields.io/badge/python-3.13-blue.svg" alt="Supported Python versions">
</a>
</p>

# Portabase Agent

## Presentation

## Memo 

If you're using Semantic Versioning (SemVer) to version your Docker images, you can use the following format:

```major.minor.patch-rc.release (e.g. 1.0.0-rc.1)```

```major.minor.patch-rc.release-tag (e.g. 1.0.0-rc.1-dev)```


docker tag agent-portabase-app solucetechnologies/agent-portabase:0.0.1-rc.1-dev
docker push solucetechnologies/agent-portabase:0.0.1-rc.1-dev


psql postgresql://devuser:changeme@localhost:5430/devdb

CREATE TABLE my_table (
id SERIAL PRIMARY KEY,
name VARCHAR(100),
age INT
);


INSERT INTO my_table (name, age)
VALUES ('John Doe', 30);