#!/bin/bash

export LC_ALL="en_US.UTF-8"
DEBIAN_FRONTEND=noninteractive
swapsize=1024

echo $1 > /etc/hostname

grep -q "swapfile" /etc/fstab
if [ $? -ne 0 ]; then
    echo 'swapfile not found. Adding swapfile.'
    fallocate -l ${swapsize}M /swapfile
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    echo '/swapfile none swap defaults 0 0' >> /etc/fstab
else
    echo 'swapfile found. No changes made.'
fi

if [ ! -f "/home/ubuntu/.pypirc" ]; then
    echo "Creating ~/.pypirc"
    cat <<'EOF' > /home/ubuntu/.pypirc
[distutils]
index-servers =
    pypicloud

[pypicloud]
repository: https://pypi.enfoldsystems.com/pypi
username: <username>
password: <password>
EOF
fi

if [ ! -d "/home/ubuntu/.buildout" ]; then
    echo "Creating ~/.buildout/default.cfg"
    mkdir -p /home/ubuntu/.buildout
    cat <<'EOF' > /home/ubuntu/.buildout/default.cfg
[buildout]
download-cache = /opt/plone/downloads
extends-cache = /opt/plone/downloads/extends
EOF
fi

if [ ! -d "/home/ubuntu/.subversion" ]; then
    echo "Creating ~/.subversion/servers"
    mkdir /home/ubuntu/.subversion
    cat <<'EOF' > /home/ubuntu/.subversion/servers
[global]
store-plaintext-passwords = yes
EOF
fi


echo "apt-get update & install system packages"
apt-get -qq update
apt-get install -yq python-dev python-apt python-setuptools \
    python-virtualenv python-pip python-magic python-tk\
    libncurses5-dev libjpeg-dev libneon27-dev libreadline-dev \
    libz-dev libxslt-dev libxml2-dev libssl-dev \
    git subversion wget curl tmux zip nodejs nodejs-legacy npm s3cmd 

echo "Wiring up npm cache"
npm config get cache

echo "Installing less, grunt, grunt-cli, brower"
npm --silent install -g less grunt grunt-cli bower

mkdir -p /opt/plone/var
mkdir -p /opt/plone/downloads/extends
mkdir -p /opt/plone/downloads/dist
mkdir -p /opt/plone/eggs


if [ ! -f "/vagrant/bin/activate" ]; then
    echo "virtualenv not found; virtualenv-ing /vagrant"
    virtualenv --always-copy -p python2.7 /vagrant
fi

if [ ! -f "/vagrant/bin/buildout" ]; then
    echo "bootstrapping buildout"
    /vagrant/bin/pip install -U setuptools==24.3.0 zc.buildout==2.5.2 pip
fi

chown -R ubuntu /home/ubuntu
chown -R ubuntu /opt/plone


echo "Finished. Reload Vagrant and Buildout."
echo "host% vagrant reload"
echo "host% vagrant ssh"
echo "host% /vagrant/bin/buildout -Nvc /vagrant/vagrant.cfg"
