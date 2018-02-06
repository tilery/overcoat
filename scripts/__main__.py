import os
import subprocess

import minicli
import requests
from usine import (cd, chown, config, connect, cp, env, exists, mkdir, put,
                   run, screen, sudo, template)


def python(cmd):
    with sudo(user='tilery'):
        run(f'/srv/tilery/venv/bin/python {cmd}')


@minicli.cli
def pip(cmd):
    with sudo(user='tilery'):
        run(f'/srv/tilery/venv/bin/pip {cmd}')


@minicli.cli
def system():
    with sudo():
        run('apt update')
        run('apt install -y postgresql-9.5 postgresql-9.5-postgis-2.2 '
            'software-properties-common wget nginx unzip autoconf libtool g++ '
            'apache2 apache2-dev libmapnik-dev libleveldb1v5 libgeos-dev '
            'libprotobuf-dev unifont curl zlib1g-dev uuid-dev python-psycopg2')
        # Prevent conflict with nginx.
        run('apt install -y apache2 apache2-dev')
        run('useradd -N tilery -d /srv/tilery/ || exit 0')
        mkdir('/srv/tilery/src')
        mkdir('/srv/tilery/tmp')
        mkdir('/srv/tilery/letsencrypt/.well-known/acme-challenge')
        chown('tilery:users', '/srv/tilery/')
        run('chsh -s /bin/bash tilery')
    install_imposm3()
    install_mod_tile()
    configure_mod_tile()
    netdata()


@minicli.cli
def netdata(force=False):
    if not exists('/etc/systemd/system/netdata.service') or force:
        run('bash <(curl -Ss https://my-netdata.io/kickstart.sh) --dont-wait')
    put('scripts/netdata.conf', '/etc/netdata/netdata.conf')
    put('scripts/tiles.chart.py',
        '/usr/libexec/netdata/python.d/tiles.chart.py')
    run('usermod -aG adm netdata')
    restart(services='netdata')


def install_imposm3(force=False):
    if exists('/usr/bin/imposm3') and not force:
        print('imposm3 already installed')
        return
    run('wget https://imposm.org/static/rel/imposm3-0.4.0dev-20170519-3f00374-linux-x86-64.tar.gz -O /tmp/imposm3.tar.gz')  # noqa
    run('tar -xzf /tmp/imposm3.tar.gz --directory /tmp')
    with sudo():
        cp('/tmp/imposm3-0.4.0dev-20170519-3f00374-linux-x86-64/imposm3',
           '/usr/bin/imposm3')
    with sudo(user='tilery'):
        mkdir('/srv/tilery/tmp/imposm')


def install_mod_tile(force=False):
    if exists('/usr/local/bin/renderd') and not force:
        print('mod_tile already installed')
        return
    run('wget https://github.com/SomeoneElseOSM/mod_tile/archive/master.zip -O /tmp/mod_tile.zip')  # noqa
    run('unzip -n /tmp/mod_tile.zip -d /tmp/')
    with cd('/tmp/mod_tile-master'):
        run('./autogen.sh')
        run('./configure')
        run('make')
        with sudo():
            run('make install')
            run('make install-mod_tile')
            run('ldconfig')
    with sudo(user='tilery'):
        mkdir('/var/run/renderd')


def configure_mod_tile():
    with sudo(user='tilery'):
        mkdir('/srv/tilery/tmp/tiles')
        mkdir('/srv/tilery/renderd')
    with sudo(), cd('/etc/apache2/'):
        put('scripts/tile.load', 'mods-available/tile.load')
        put('scripts/tile.conf', 'mods-available/tile.conf')
        put('scripts/apache.conf', 'sites-enabled/000-default.conf')
        put('scripts/ports.conf', 'ports.conf')
        run('a2enmod tile')


@minicli.cli
def db():
    with sudo(user='postgres'):
        run('createuser tilery || exit 0')
        run('createdb tilery -O tilery || exit 0')
        run('psql tilery -c "CREATE EXTENSION IF NOT EXISTS postgis"')


@minicli.cli
def http():
    # When we'll have a domain.
    put('scripts/letsencrypt.conf', '/etc/nginx/snippets/letsencrypt.conf')
    put('scripts/ssl.conf', '/etc/nginx/snippets/ssl.conf')
    domains = ' '.join(config.domains)
    domain = config.domains[0]
    pempath = f'/etc/letsencrypt/live/{domain}/fullchain.pem'
    if exists(pempath):
        print(f'{pempath} found, using https configuration')
        conf = template('scripts/nginx-https.conf', domains=domains,
                        domain=domain)
    else:
        print(f'{pempath} not found, using http configuration')
        # Before letsencrypt.
        conf = template('scripts/nginx-http.conf', domains=domains,
                        domain=domain)
    put(conf, '/etc/nginx/sites-enabled/default')
    restart()


@minicli.cli
def bootstrap():
    system()
    db()
    services()
    http()
    letsencrypt()
    # Now put the https ready Nginx conf.
    http()
    ssh_keys()


@minicli.cli
def letsencrypt():
    with sudo():
        run('add-apt-repository --yes ppa:certbot/certbot')
        run('apt update')
        run('apt install -y certbot')
    certbot_conf = template('scripts/certbot.ini',
                            domains=','.join(config.domains))
    put(certbot_conf, '/srv/tilery/certbot.ini')
    put('scripts/ssl-renew', '/etc/cron.weekly/ssl-renew')
    run('chmod +x /etc/cron.weekly/ssl-renew')
    run('certbot certonly -c /srv/tilery/certbot.ini --non-interactive '
        '--agree-tos')


@minicli.cli
def services():
    service('renderd')
    service('imposm')


def service(name):
    put(f'scripts/{name}.service', f'/etc/systemd/system/{name}.service')
    run(f'systemctl enable {name}.service')


@minicli.cli
def ssh_keys():
    with sudo():
        for name, url in config.get('ssh_key_urls', {}).items():
            key = requests.get(url).text.replace('\n', '')
            run('grep -q -r "{key}" .ssh/authorized_keys || echo "{key}" '
                '| tee --append .ssh/authorized_keys'.format(key=key))


def export(flavour='forte', filename='forte', lang='fr'):
    env = os.environ.copy()
    env['PIANOFORTE_LANG'] = lang
    subprocess.call(['node', '/home/ybon/Code/js/kosmtik/index.js', 'export',
                     f'{flavour}.yml', '--format', 'xml', '--output',
                     f'{filename}.xml', '--localconfig',
                     'localconfig-remote.js'], env=env)


@minicli.cli
def deploy():
    """Send config files."""
    flavours = [
        ('forte', 'forte', 'fr'),
        ('piano', 'piano', 'fr'),
        ('forte', 'forteen', 'en'),
        ('piano', 'pianoen', 'en'),
        ('forte', 'fortear', 'ar'),
        ('piano', 'pianoar', 'ar'),
    ]
    with sudo(user='tilery'):
        mkdir('/srv/tilery/pianoforte/data')
        put('mapping.yml', '/srv/tilery/mapping.yml')
        imposm_conf = template('scripts/imposm.conf', **config)
        put(imposm_conf, '/srv/tilery/imposm.conf')
        put('scripts/renderd.conf', '/srv/tilery/renderd.conf')
        put('scripts/www', '/srv/tilery/www')
        index = template('scripts/www/index.html', **config)
        put(index, '/srv/tilery/www/index.html')
        for flavour, name, lang in flavours:
            export(flavour, name, lang)
            put(f'{name}.xml', f'/srv/tilery/pianoforte/{name}.xml')
        put('data/country.csv', '/srv/tilery/pianoforte/data/country.csv')
        put('data/city.csv', '/srv/tilery/pianoforte/data/city.csv')
        put('data/simplified_boundary.json',
            '/srv/tilery/pianoforte/data/simplified_boundary.json')
        put('data/disputed.json', '/srv/tilery/pianoforte/data/disputed.json')
        put('fonts/', '/srv/tilery/pianoforte/fonts')
        put('icon/', '/srv/tilery/pianoforte/icon')


def download_shapefile(name, url, force):
    datapath = '/srv/tilery/data/'
    if not exists(datapath + name) or force:
        run(f'wget {url} -O /tmp/data.zip --quiet')
        run(f'unzip -n /tmp/data.zip -d {datapath}')


@minicli.cli
def download(force=False):
    path = '/srv/tilery/tmp/data.osm.pbf'
    if not exists(path) or force:
        url = config.download_url
        run(f'wget {url} -O {path} --quiet')
    domain = 'http://data.openstreetmapdata.com/'
    download_shapefile(
        'simplified-land-polygons-complete-3857/simplified_land_polygons.shp',
        f'{domain}simplified-land-polygons-complete-3857.zip', force)
    download_shapefile('land-polygons-split-3857/land_polygons.shp',
                       f'{domain}land-polygons-split-3857.zip', force)
    domain = 'http://nuage.yohanboniface.me/'
    download_shapefile('boundary_lines/boundary_lines_simplified.shp',
                       f'{domain}boundary_lines_simplified.zip', force)
    download_shapefile('boundary_lines_simplified/boundary_lines.shp',
                       f'{domain}boundary_lines.zip', force)


@minicli.cli(name='import')
def import_data(remove_backup=False):
    with sudo(user='tilery'), env(PGHOST='/var/run/postgresql/'):
        if remove_backup:
            run('imposm3 import -config /srv/tilery/imposm.conf -removebackup')
        with screen():
            run('imposm3 import -diff -config /srv/tilery/imposm.conf '
                '-read /srv/tilery/tmp/data.osm.pbf -overwritecache '
                '-write -deployproduction 2>&1 | tee /tmp/imposm.log')
        run('tail -F /tmp/imposm.log')


@minicli.cli
def systemctl(cmd):
    run(f'systemctl {cmd}')


@minicli.cli
def logs(lines=50, services=None):
    if not services:
        services = 'renderd apache2 nginx imposm'
    services = ' --unit '.join(services.split())
    run(f'journalctl --lines {lines} --unit {services}')


@minicli.cli
def access():
    run('tail -F /var/log/nginx/access.log')


@minicli.cli
def psql(query):
    with sudo(user='postgres'):
        run(f'psql tilery -c "{query}"')


@minicli.cli
def clear_cache():
    run('rm -rf /srv/tilery/tmp/tiles/*')


@minicli.cli
def restart(services=None):
    services = services or 'renderd apache2 nginx imposm'
    run('sudo systemctl restart {}'.format(services))


@minicli.cli
def render(map='piano', min=1, max=10):
    with sudo(user='tilery'), screen():
        run(f'render_list --map {map} --all --force --num-threads 8 '
            f'--socket /var/run/renderd/renderd.sock '
            f'--tile-dir /srv/tilery/tmp/tiles '
            f' --min-zoom {min} --max-zoom {max}')


@minicli.cli
def import_sql():
    names = ['boundary', 'city', 'country']
    for name in names:
        path = f'/srv/tilery/tmp/{name}.sql'
        with sudo(user='tilery'):
            put(f'tmp/{name}.sql', path)
            run(f'psql --single-transaction -d tilery --file {path}')


@minicli.wrap
def wrapper(hostname, configpath):
    with connect(hostname=hostname, configpath=configpath):
        yield


if __name__ == '__main__':
    minicli.run(hostname='pianoforteqa', configpath='usine.yml')
