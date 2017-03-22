# Provisioning a New Site

## Required Packages

- Nginx
- Python 3.6
- Git
- pip
- virtualenv

e.g. On Ubuntu:

```bash
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get install nginx git python36 python3.6-venv
```

## Nginx Virtual Host Config

* See [nginx.template.conf](nginx.template.conf).
* Replace `SITENAME` with, e.g. _example.domain.com_.

## Systemd Service

* See [gunicorn-systemd.template.service](gunicorn-systemd.template.service)
* Replace `SITENAME` with, e.g. _staging.domain.com_.

## Folder Structure

Assume we have a user account at `/home/username`.

```
/home/username
└── sites
    └── SITENAME
        ├── database
        ├── source
        ├── static
        └── virtualenv
```
