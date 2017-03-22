from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/joegnis/superlists'


def deploy():
    site_dir = f'/home/{env.user}/sites/{env.host}'
    source_dir = site_dir + '/source'
    _create_dir_structure_if_necessary(site_dir)
    _get_latest_source(source_dir)
    _update_settings(source_dir, env.host)
    _update_static_files(source_dir)
    _update_virtualenv(source_dir)
    _update_static_files(source_dir)
    _update_database(source_dir)


def _create_dir_structure_if_necessary(site_dir):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_dir}/{subfolder}')


def _get_latest_source(source_dir):
    if exists(source_dir + '/.git'):
        run(f'cd {source_dir} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_dir}')
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'cd {source_dir} && git reset --hard {current_commit}')


def _update_settings(source_dir, site_name):
    settings_path = source_dir + '/superlists/settings.py'
    sed(settings_path, 'Debug = True', 'Debug = False')
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
    )
    secret_key_file = source_dir + '/superlists/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz01234567890!@#$%^&*()-_=+'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f"SECRET_KEY = '{key}'")
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_dir):
    virtualenv_dir = source_dir + '/../virtualenv'
    if not exists(virtualenv_dir + '/bin/pip'):
        run(f'python3.6 -m venv {virtualenv_dir}')
    run(f'{virtualenv_dir}/bin/pip install -r {source_dir}/requirements.txt')


def _update_static_files(source_dir):
    run(f'cd {source_dir} && ../virtualenv/bin/python manage.py collectstatic --noinput')


def _update_database(source_dir):
    run(f'cd {source_dir} && ../virtualenv/bin/python manage.py migrate --noinput')
