#!/bin/bash

# escopo
# mudando para o diretorio do projeto
var="$0"
name=${var##*/}
directory=$(echo "$0" | sed "s/$name//")
cd $directory
# variáveis de escopo
db_dir="bancos"
db_name="homelab.db"
db="../$db_dir/$db_name"
file="create_homelab_database.sql"

# funções
path(){
  cond=$(pwd | sed -r "s/[//]/\n/g" | grep -i home_lab)
  if [[ -z $cond ]]; then
    echo "Erro, Entre no path do projeto homelab."
    exit 1;
  fi;
};

drop(){
  path;
  tables=$(sqlite3 $db ".tables")
  for i in $tables; do
     sqlite3 $db "drop table "$i;
  done;
};

create(){
  path;
  sqlite3 $db  ".read "$file > /dev/null 2>&1
#  aux=$?
#  echo "${?}"
  if [[ $? == "1" ]]; then
    echo "tabelas já existem no banco, nenhuma alteração foi feita."
  fi
#  echo "${?}"
  exit 0;
}
# fim funções

# ===============script===============
cont=0
for i in $@; do
  cont=$(($cont + 1))
done


if [[ cont -gt $((1)) ]]; then
  echo "erro: numero de inputs maior que 1."
  echo "use: bd.sh"
  exit 1;

elif [[ cont -lt $((1)) ]]; then
  echo "passe um input:(drop ou create)"
  exit 0;
fi;


if [[ $1 == "drop" ]]; then
    #echo "";
    drop;

elif [[ $1 == "create" ]]; then
    #echo "";
    create;

fi;
