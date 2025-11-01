<!-- PROJECT LOGO -->

[//]: # (<br />)

[//]: # (<div align="center">)

[//]: # (  <a href="https://github.com/othneildrew/Best-README-Template">)

[//]: # (    <img src="images/logo.png" alt="Logo" width="80" height="80">)

[//]: # (  </a>)

<h3 align="center">Portabase Agent</h3>

<p align="center">
<a href="https://www.python.org/downloads/release/python-3120/" target="_blank">
    <img src="https://img.shields.io/badge/python-3.13-blue.svg" alt="Supported Python versions">
</a>
</p>


  <p align="center">
    Backup / Restore your databases instances
    <br />
    <a href="https://portabase.net"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://portabase.net">View Demo</a>
    ·
    <a href="https://github.com/Soluce-Technologies/agent-portabase/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/Soluce-Technologies/agent-portabase/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>


<!-- ABOUT THE PROJECT -->

## About The Project

Portabase Agent is the agent service use with Portabase Server. This service is for backup/restore db instances.
<a href="https://github.com/Soluce-Technologies/portabase">Portabase Server</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][Python]][Python-url]
* [![Celery][Celery]][Celery-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

Sync your uv config

* npm
  ```sh
  uv sync
  ```

### Installation

Installation steps in order to use it locally and work on some features improvements

1. Clone the repo
   ```sh
   git clone https://github.com/Soluce-Technologies/agent-portabase
   ```
3. Start the project
   ```sh
   docker compose up 
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ROADMAP -->

## Roadmap

- [ ] Add Changelog
- [ ] Add tests procedure
- [ ] Add Release File
- [ ] Security improvements
- [ ] Multi db support
    - [x] PostgreSQL
    - [ ] MongoDB
    - [ ] MySQL

See the [open issues](https://github.com/Soluce-Technologies/agent-portabase/issues) for a full list of proposed
features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Database Test Seed

Using Docker

### For postgres
```bash
docker exec -i -e PGPASSWORD=<password> <container_name> psql -U <USER> -d <DATABASE> < ./scripts/seed.sql
```
### For mysql 
install the client cli before

```bash
mysql -h 127.0.0.1 -P <port> -u <username> -p<password> <database_name> < ./scripts/seed.sql
```

<!-- CONTRIBUTING -->

## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any
contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also
simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Top contributors:

<a href="https://github.com/Soluce-Technologies/agent-portabase/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=Soluce-Technologies/agent-portabase" alt="contrib.rocks image" />
</a>

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Memo

If you're using Semantic Versioning (SemVer) to version your Docker images, you can use the following format:

```major.minor.patch-rc.release (e.g. 1.0.0-rc.1)```

```major.minor.patch-rc.release-tag (e.g. 1.0.0-rc.1-dev)```


<!-- LICENSE -->

## License

Distributed under the Apache License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- CONTACT -->

## Contact

Killian Larcher - killian.larcher@soluce-technologies.com
Charles Gauthereau - charles.gauthereau@soluce-technologies.com

Project
Link: [https://github.com/Soluce-Technologies/agent-portabase](https://github.com/Soluce-Technologies/agent-portabase)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54

[Celery]: https://img.shields.io/static/v1?style=for-the-badge&message=Celery&color=37814A&logo=Celery&logoColor=FFFFFF&label

[Python-url]: https://www.python.org/

[Celery-url]: https://docs.celeryq.dev/en/stable/