-- ==========================================================
-- SCRIPT DE CREACION DE BASE DE DATOS Y TABLAS - SEMANA 9
-- CLINICA SALUDTOTAL - EVALUACION FINAL PROGRAMACION AVANZADA
-- Creado por: Claudio Baeza H.
-- ==========================================================

-- 1. Crear la base de datos si no existe
CREATE DATABASE IF NOT EXISTS clinica_saludtotal
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- 2. Seleccionar la base de datos para usarla
USE clinica_saludtotal;

-- 3. Crear la tabla de Pacientes
DROP TABLE IF EXISTS Pacientes;
CREATE TABLE Pacientes (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    RUT VARCHAR(15) NOT NULL UNIQUE,
    NumFicha VARCHAR(20) NOT NULL UNIQUE,
    Nombre VARCHAR(100) NOT NULL,
    Edad INT,
    Genero VARCHAR(10),
    HistorialMedico TEXT,
    Telefono VARCHAR(20),
    Correo VARCHAR(100),
    Especialidad VARCHAR(50),
    Estado VARCHAR(30),
    FechaIngreso DATETIME
);

-- 4. Insertar los registros de prueba solicitados
INSERT INTO Pacientes (RUT, NumFicha, Nombre, Edad, Genero, HistorialMedico, Telefono, Correo, Especialidad, Estado, FechaIngreso) VALUES
('11.111.111-1', 'F-2026-8452', 'Juan Perez', 35, 'Masculino', 'Hipertensión - Tratamiento: Losartán 50mg', '+56912345678', 'juan@example.com', 'Medicina General', 'En Tratamiento', NOW()),
('22.222.222-2', 'F-2026-1023', 'María López', 45, 'Femenino', 'Diabetes - Tratamiento: Metformina', '+56987654321', 'maria@example.com', 'Endocrinología', 'En Tratamiento', NOW()),
('33.333.333-3', 'F-2026-9912', 'Pedro García', 28, 'Masculino', 'Asma - Tratamiento: Salbutamol', '+56911223344', 'pedro@example.com', 'Broncopulmonar', 'Alta Médica', NOW());

-- 5. Consulta de verificacion (Opcional, para verificar en phpMyAdmin)
SELECT * FROM Pacientes;
