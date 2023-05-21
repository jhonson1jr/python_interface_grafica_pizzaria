create database bd_curso_python;
use bd_curso_python;

create table tb_cadastros(
	id integer unsigned auto_increment not null,
    nome varchar(255) null,
    senha varchar(255) null,
    nivel int unsigned null,
    constraint pk_tb_cadastros primary key (id)
);

insert into tb_cadastros(nome, senha, nivel) values ('admin', 'admin', 2);
insert into tb_cadastros(nome, senha, nivel) values ('usuario', 'admin', 1);

create table tb_produtos(
	id integer unsigned auto_increment not null,
    nome varchar(255) null,
    ingredientes varchar(255) null,
    grupo varchar(255) null,
    preco decimal(5,2) null,
    constraint pk_tb_produtos primary key (id)
);

INSERT INTO `tb_produtos` (`nome`, `ingredientes`, `grupo`, `preco`) VALUES ('Pizza Mussarela', 'massa, mussarela', 'pizzas', '33.5');
INSERT INTO `tb_produtos` (`nome`, `ingredientes`, `grupo`, `preco`) VALUES ('Coca Cola', '', 'bebidas', '6');
INSERT INTO `tb_produtos` (`nome`, `ingredientes`, `grupo`, `preco`) VALUES ('Pizza Portuguesa', 'massa, mussarela, presunto, ovo', 'pizzas', '35.5');
INSERT INTO `tb_produtos` (`nome`, `grupo`, `preco`) VALUES ('Suco Laranja', 'bebidas', '7.5');

create table tb_pedidos(
	id integer unsigned auto_increment not null,
    nome varchar(255) null,
    ingredientes varchar(255) null,
    grupo varchar(255) null,
    localEntrega varchar(255) null,
    observacoes varchar(255) null,    
    constraint pk_tb_pedidos primary key (id)
);

insert into tb_pedidos (nome, ingredientes, grupo, localEntrega, observacoes) values ('Pizza Mussarela', 'mussarela', 'pizzas', '', 'sem cebola');
insert into tb_pedidos (nome, ingredientes, grupo, localEntrega, observacoes) values ('Coca Cola', '', 'bebidas', '', 'gelada');

create table tb_estatisticas_vendas(
	id integer unsigned auto_increment not null,
    nome varchar(255) null,
    grupo varchar(255) null,
    preco decimal(5,2) null,
    constraint pk_tb_estatisticas_vendas primary key (id)
);


insert into tb_estatisticas_vendas (nome, grupo, preco) values ('Pizza Mussarela', 'pizzas', 34.9);
insert into tb_estatisticas_vendas (nome, grupo, preco) values ('Coca Cola', 'bebidas', 6);
insert into tb_estatisticas_vendas (nome, grupo, preco) values ('Pizza Portuguesa', 'pizzas', 34.9);
insert into tb_estatisticas_vendas (nome, grupo, preco) values ('Suco Laranja', 'bebidas', 7.5);
insert into tb_estatisticas_vendas (nome, grupo, preco) values ('Suco Laranja', 'bebidas', 7.5);
