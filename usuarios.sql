
-- =====================================================
-- SEGURIDAD VIAL SOACHA
-- MOTOR: SQLITE
-- =====================================================

PRAGMA foreign_keys = ON;

-- =====================================================
-- TABLA DE USUARIOS
-- =====================================================

CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cedula TEXT UNIQUE NOT NULL,
    nombre TEXT NOT NULL,
    edad INTEGER NOT NULL,
    correo TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    direccion TEXT NOT NULL,
    barrio TEXT NOT NULL,
    localidad TEXT NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLA DE REPORTES Y PQR
-- =====================================================

CREATE TABLE IF NOT EXISTS reportes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    correo_usuario TEXT NOT NULL,
    pqr_codigo TEXT UNIQUE NOT NULL,
    descripcion TEXT NOT NULL,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (usuario_id)
        REFERENCES usuarios(id)
);

-- =====================================================
-- ÍNDICE PARA CONSULTAS DE HISTORIAL
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_reportes_usuario
ON reportes(usuario_id);
