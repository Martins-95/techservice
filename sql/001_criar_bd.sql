DROP DATABASE IF EXISTS techservice_db;

CREATE DATABASE techservice_db;

USE techservice_db;

CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    telefone VARCHAR(20),
    nif VARCHAR(20) UNIQUE,
    morada VARCHAR(200),
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    deleted_at DATETIME NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Tabela Equipamentos
CREATE TABLE equipamentos (
    id_equipamento INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    tipo VARCHAR(50) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(50) NOT NULL,
    numero_serie VARCHAR(100) NOT NULL UNIQUE,
    data_compra DATE NULL,
    status TINYINT NOT NULL DEFAULT 1,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    deleted_at DATETIME NULL,
    CONSTRAINT fk_equipamentos_clientes 
        FOREIGN KEY (id_cliente) 
        REFERENCES clientes(id_cliente) 
        ON UPDATE CASCADE 
        ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Tabela Dominio: Status da Ordem de Servico
CREATE TABLE status_ordem (
    id_status INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE,
    descricao VARCHAR(150)
);

INSERT INTO status_ordem (id_status, nome, descricao) VALUES
(1, 'Aberta', 'Ordem de serviço registada no sistema'),
(2, 'Em Andamento', 'Equipamento em diagnóstico ou reparação'),
(3, 'Aguardando Peças', 'Aguardando chegada de componentes'),
(4, 'Concluída', 'Serviço finalizado com sucesso'),
(5, 'Cancelada', 'Serviço cancelado');

-- 4. Tabela Ordens de Servico
CREATE TABLE ordens_servico (
    id_ordem INT AUTO_INCREMENT PRIMARY KEY,
    id_equipamento INT NOT NULL,
    id_status INT NOT NULL DEFAULT 1,
    defeito_relatado VARCHAR(500) NOT NULL,
    diagnostico VARCHAR(500),
    solucao VARCHAR(500),
    prioridade ENUM('BAIXA', 'MEDIA', 'ALTA') DEFAULT 'MEDIA',
    valor_servico DECIMAL(10,2) DEFAULT 0.00,
    valor_pecas DECIMAL(10,2) DEFAULT 0.00,
    desconto DECIMAL(10,2) DEFAULT 0.00,
    valor_total DECIMAL(10,2) DEFAULT 0.00,
    observacoes VARCHAR(300),
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NULL,
    FOREIGN KEY (id_equipamento) REFERENCES equipamentos(id_equipamento) ON UPDATE CASCADE ON DELETE RESTRICT,
    FOREIGN KEY (id_status) REFERENCES status_ordem(id_status) ON UPDATE CASCADE ON DELETE RESTRICT
);

-- 5. Tabela Histórico da Ordem de Servico
CREATE TABLE historico_ordem_servico (
    id_historico INT AUTO_INCREMENT PRIMARY KEY,
    id_ordem INT NOT NULL,
    id_status_anterior INT,
    id_status_novo INT NOT NULL,
    observacao VARCHAR(300),
    data_alteracao DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    usuario VARCHAR(100) DEFAULT 'Sistema',
    FOREIGN KEY (id_ordem) REFERENCES ordens_servico(id_ordem) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (id_status_anterior) REFERENCES status_ordem(id_status),
    FOREIGN KEY (id_status_novo) REFERENCES status_ordem(id_status)
);