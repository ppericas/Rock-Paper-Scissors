-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-03-2024 a las 17:16:59
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `piedra_papel_tijeras`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `Nick` varchar(30) NOT NULL,
  `Mail` varchar(50) NOT NULL,
  `Contraseña` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`Nick`, `Mail`, `Contraseña`) VALUES
('Nick_Ejemplo', 'ejemplo@ejemplo.com', '1234'),
('prueba1', 'prueba1@prueba.com', 'pbkdf2:sha256:260000$L4JeW3FGzU8c1iNh$d6599504b0c2243b5ddaa9998a638ff403cc30283e7d69e3a0f1fb93c50ad5b9'),
('prueba2', 'prueba2@prueba.com', 'pbkdf2:sha256:260000$KsjysEPlB9FsVob7$1457958731f7b89219ff887cfdb6f06602304de68c42c3b94ff94f5872fe0438'),
('prueba3', 'prueba3@prueba.com', 'pbkdf2:sha256:260000$6wm2X3hMHJ9F9lBq$f82881beb2977461ab9d2fa934661395f31ab40918bacb96febafec548a5f0a8');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`Nick`),
  ADD UNIQUE KEY `Mail` (`Mail`),
  ADD KEY `Mail_2` (`Mail`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
