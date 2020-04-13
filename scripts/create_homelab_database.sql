create table usuario(
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    login TEXT NOT NULL,
    senha TEXT NOT NULL,
    email TEXT NOT NULL,
    idAdm INTEGER,
    FOREIGN KEY(idAdm) references usuario(id)
);

create table dispositivo(
    id INTEGER NOT NULL PRIMARY KEY,
    funcao INTEGER NOT NULL,
    idPermissao INTEGER NOT NULL,
    FOREIGN KEY(idPermissao) references permissao(id)
);

create table arquivo(
    id INTEGER NOT NULL PRIMARY KEY,
    nomeArquivo TEXT NOT NULL,
    path TEXT NOT NULL,
    tipoArquivo TEXT NULL,
    idPermissao INTEGER NOT NULL,
    FOREIGN KEY(idPermissao) references permissao(id)
);

create table arquivoTags(
    idArquivo INTEGER NOT NULL,
    idTag INTEGER NOT NULL,
    tag TEXT NOT NULL,
    PRIMARY KEY(idArquivo, idTag)
);

create table permissao(
    id INTEGER NOT NULL PRIMARY KEY,
    nivelRestricao INTEGER NOT NULL
);

create table usuario_arquivo(
    idUsuario INTEGER NOT NULL,
    idArquivo INTEGER NOT NULL,
    PRIMARY KEY(idUsuario, idArquivo),
    FOREIGN KEY(idUsuario) references usuario(id),
    FOREIGN KEY(idArquivo) references arquivo(id)
);

create table usuario_dispositivo(
    idUsuario INTEGER NOT NULL,
    idDispositivo INTEGER NOT NULL,
    PRIMARY KEY(idUsuario, idDispositivo),
    FOREIGN KEY(idUsuario) references usuario(id),
    FOREIGN KEY(idDispositivo) references dispositivo(id)
);

create table usuario_permissao(
    idUsuario INTEGER NOT NULL,
    idPermissao INTEGER NOT NULL,
    PRIMARY KEY(idUsuario, idPermissao),
    FOREIGN KEY(idUsuario) references usuario(id),
    FOREIGN KEY(idPermissao) references permissao(id)
);