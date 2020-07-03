#!/bin/bash

system_account=homelab

#apt-get install python3-venv

#user=$(ps -eo "%u%c" | grep nginx | grep -v "root" | cut -f1 -d" ")
#kill $(ps -eo "%p%c" | grep nginx | cut -f1 -d" ")
# verifica se o user possui nginx

# entra na pasta do script para fazer a instalação a partir de lá.
dir=$(dirname $0)
cd $dir
#cd ..
#header=$(python3 -c "import HomeLab; print(HomeLab.__name__ + ' ' + HomeLab.__version__)")
#cd -
header="HomeLab v0.1.2"
echo "[Instalação do projeto $header]"
echo "As seguintes dependências serão instaladas:"
echo "nginx, python3-venv, uwsgi, flask e sqlalchemy."
echo "Deseja continuar ? [Y/n]: "
read cond

if [[ ! -z $cond || -n $(echo $cond | grep '[y-Y]') ]]; then
  # cancela a instalação.
	exit 0;
fi

echo "instalando dependências para HomeLab..."


# NGINX

echo "[instalando nginx]"
echo "verificando existência do nginx.."
nginx -v 2> /dev/null

if [[ $? != 0 ]]; then
  echo "tentando instalar nginx..."
  apt-get install nginx
else
  echo "$(nginx -v) se encontra no sistema, pulando etapa de instalação..."
fi;
echo ""
## NGINX FIM

# VENV

echo "[instalando python3-venv]"
echo "verificando existência de python3-venv..."
python3 -c "import venv" 2> /dev/null # verifica a existência do venv;

if [[ $? == 1 ]]; then
  echo "tentando instalar python3-venv"
  apt-get install python3-venv
else
  echo "python3-venv se encontra no sistema, pulando etapa de instalação..."
fi
echo ""
# VENV FIM

# CONFIGURACAO DO PROJETO.
echo "criando um venv python..."
python3 -m venv ../env
echo "iniciando venv..."
. ../env/bin/activate
echo "[instalando pacotes uwsgi, flask e sqlalchemy]"
pip3 install flask sqlalchemy uwsgi #-r requeriments #
echo ""
echo "movendo projeto homelab para /var/www/homelab/"
cp -R ../ /var/www/homelab

# USER HOMELAB
echo "criando system user(homelab)..."
useradd -r -d /var/www/homelab -s /bin/false homelab #$system_account
usermod -a -G homelab homelab

echo "verificando nginx system user..."
# inicia nginx e tenta recuperar o nome do usuário
nginx 2> /dev/null;
user=$(ps -aux | grep nginx | grep -E -v "root|$(whoami)" |tr -s "[:space:]" | head -n 1 | cut -f1 -d " ")
#pid=$(ps -aux | grep nginx | grep -E "root|$(whoami)" |tr -s "[:space:]" | head -n 1 | cut -f2 -d " ")

killall nginx
if [[ -z $user ]]; then
	echo "[não foi encontrado o system user de nginx]"
	exit 1;
fi
echo "nginx system user: "$user
echo "adicionando nginx user($user) ao group homelab..."
usermod -a -G homelab $user
chown -R homelab:homelab /var/www/homelab
#chmod -R 660 /var/www/homelab
chmod 750 /var/www/homelab

# cp as configurações do nginx.conf e homelab.conf

cp -b /etc/nginx/nginx.conf /etc/nginx/nginx.conf.orig
cp -b nginx.conf /etc/nginx/nginx.conf
cp -b homelab.conf /etc/nginx/conf.d/homelab.conf

echo "criando servico homelab.service ..."
cp ./homelab.service /etc/systemd/system/homelab.service
echo "iniciando serviços homelab e nginx."
systemctl daemon-reload
systemctl enable homelab
systemctl enable nginx
systemctl start homelab nginx
echo "para finalizar utilize systemctl stop homelab nginx"
echo "instalação finalizada !"

# USER FIM