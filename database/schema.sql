CREATE DATABASE IF NOT EXISTS horisoft
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE horisoft;


-- =====================================================
-- 1. USUARIOS
-- =====================================================

CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    documento VARCHAR(30) NOT NULL UNIQUE,
    correo VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(30),
    password VARCHAR(255) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    apartamento VARCHAR(20),
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =====================================================
-- 2. PAGOS
-- =====================================================

CREATE TABLE pagos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    valor DECIMAL(12,2) NOT NULL,
    fecha DATE NOT NULL,
    estado VARCHAR(30) DEFAULT 'Pendiente',

    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- =====================================================
-- 3. PQRS
-- =====================================================

CREATE TABLE pqrs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    tipo VARCHAR(30) NOT NULL,
    asunto VARCHAR(150) NOT NULL,
    descripcion TEXT NOT NULL,
    estado VARCHAR(30) DEFAULT 'Pendiente',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- =====================================================
-- 4. COMUNICADOS
-- =====================================================

CREATE TABLE comunicados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    mensaje TEXT NOT NULL,
    fecha DATE NOT NULL,
    estado VARCHAR(30) DEFAULT 'Publicado',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =====================================================
-- 5. CONFIGURACION
-- =====================================================

CREATE TABLE configuracion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_conjunto VARCHAR(150) NOT NULL,
    direccion VARCHAR(200),
    telefono VARCHAR(30),
    correo VARCHAR(100),
    nit VARCHAR(50),
    administrador VARCHAR(100)
);


-- =====================================================
-- 6. CUENTAS DE COBRO
-- =====================================================

CREATE TABLE cuentas_cobro (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    periodo VARCHAR(20) NOT NULL,
    valor DECIMAL(12,2) NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    estado VARCHAR(30) DEFAULT 'Pendiente',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- =====================================================
-- 7. DOCUMENTOS
-- =====================================================

CREATE TABLE documentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    tipo VARCHAR(100),
    ruta VARCHAR(500),
    fecha DATE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =====================================================
-- 8. PROVEEDORES
-- =====================================================

CREATE TABLE proveedores (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    nit VARCHAR(50) NOT NULL UNIQUE,
    telefono VARCHAR(30),
    correo VARCHAR(100),
    direccion VARCHAR(200),
    estado VARCHAR(30) DEFAULT 'Activo',
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- =====================================================
-- 9. INVENTARIO
-- =====================================================

CREATE TABLE inventario (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    descripcion VARCHAR(255),
    cantidad INT NOT NULL DEFAULT 0,
    unidad VARCHAR(30),
    stock_minimo INT DEFAULT 0,
    proveedor_id INT,
    estado VARCHAR(30) DEFAULT 'Disponible',

    FOREIGN KEY (proveedor_id)
        REFERENCES proveedores(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);


-- =====================================================
-- 10. VEHICULOS
-- =====================================================

CREATE TABLE vehiculos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    placa VARCHAR(20) NOT NULL UNIQUE,
    marca VARCHAR(50),
    modelo VARCHAR(50),
    color VARCHAR(30),
    tipo VARCHAR(50),
    estado VARCHAR(30) DEFAULT 'Activo',

    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- =====================================================
-- 11. VIGILANTES
-- =====================================================

CREATE TABLE vigilantes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    documento VARCHAR(30) NOT NULL UNIQUE,
    telefono VARCHAR(30),
    turno VARCHAR(50),
    estado VARCHAR(30) DEFAULT 'Activo',
    fecha_ingreso DATE
);


-- =====================================================
-- 12. ZONAS COMUNES
-- =====================================================

CREATE TABLE zonas_comunes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion VARCHAR(255),
    capacidad INT,
    estado VARCHAR(30) DEFAULT 'Disponible'
);


-- =====================================================
-- 13. RESERVAS
-- =====================================================

CREATE TABLE reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    zona_id INT NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    estado VARCHAR(30) DEFAULT 'Pendiente',
    observaciones VARCHAR(255),

    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (zona_id)
        REFERENCES zonas_comunes(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);


-- =====================================================
-- DATOS INICIALES
-- =====================================================

INSERT INTO configuracion
(nombre_conjunto, direccion, telefono, correo, nit, administrador)
VALUES
(
    'Conjunto Residencial HORISOFT',
    'Bogotá, Colombia',
    '3000000000',
    'administracion@horisoft.com',
    '900000000-1',
    'Administrador General'
);


INSERT INTO usuarios
(nombre, documento, correo, telefono, password, rol, apartamento, estado)
VALUES
(
    'Administrador',
    '1000000001',
    'admin@horisoft.com',
    '3000000000',
    '123456',
    'Administrador',
    'ADMIN',
    'Activo'
);


INSERT INTO usuarios
(nombre, documento, correo, telefono, password, rol, apartamento, estado)
VALUES
(
    'Usuario Residente',
    '1000000002',
    'residente@horisoft.com',
    '3000000001',
    '123456',
    'Residente',
    '101',
    'Activo'
);


INSERT INTO zonas_comunes
(nombre, descripcion, capacidad, estado)
VALUES
('Salón Comunal', 'Espacio para reuniones y eventos', 50, 'Disponible');


INSERT INTO zonas_comunes
(nombre, descripcion, capacidad, estado)
VALUES
('Zona BBQ', 'Zona para reuniones familiares', 20, 'Disponible');


INSERT INTO zonas_comunes
(nombre, descripcion, capacidad, estado)
VALUES
('Cancha Deportiva', 'Espacio deportivo del conjunto', 30, 'Disponible');


INSERT INTO proveedores
(nombre, nit, telefono, correo, direccion)
VALUES
(
    'Proveedor General HORISOFT',
    '900111222-3',
    '3100000000',
    'proveedor@horisoft.com',
    'Bogotá, Colombia'
);


INSERT INTO inventario
(nombre, descripcion, cantidad, unidad, stock_minimo, proveedor_id)
VALUES
(
    'Bombillos LED',
    'Bombillos para zonas comunes',
    20,
    'Unidades',
    5,
    1
);


INSERT INTO inventario
(nombre, descripcion, cantidad, unidad, stock_minimo, proveedor_id)
VALUES
(
    'Escobas',
    'Elementos de aseo',
    10,
    'Unidades',
    3,
    1
);