-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Sep 10, 2025 at 11:51 PM
-- Server version: 8.4.3
-- PHP Version: 8.3.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `soportes-uptamca`
--

-- --------------------------------------------------------

--
-- Table structure for table `departamentos`
--

CREATE TABLE `departamentos` (
  `id` int NOT NULL,
  `nombre` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `departamentos`
--

INSERT INTO `departamentos` (`id`, `nombre`) VALUES
(1, 'Despacho del Contralor'),
(2, 'Dirección de Talento Humano'),
(3, 'Dirección de Tecnología de Información y Comunicaciones'),
(4, 'Oficina de Atención al Ciudadano');

-- --------------------------------------------------------

--
-- Table structure for table `personal`
--

CREATE TABLE `personal` (
  `id` int NOT NULL,
  `cedula` varchar(50) NOT NULL,
  `nombre` varchar(255) NOT NULL,
  `apellido` varchar(255) NOT NULL,
  `id_departamento` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `personal`
--

INSERT INTO `personal` (`id`, `cedula`, `nombre`, `apellido`, `id_departamento`) VALUES
(1, '85438548', 'jose', 'martinez', 4),
(2, '737278', 'Armando', 'Carrera', 5),
(3, '28405147', 'miguel', 'martinez', 1);

-- --------------------------------------------------------

--
-- Table structure for table `rol`
--

CREATE TABLE `rol` (
  `id` int NOT NULL,
  `tipo` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `rol`
--

INSERT INTO `rol` (`id`, `tipo`) VALUES
(1, 'Administrador'),
(2, 'Técnico');

-- --------------------------------------------------------

--
-- Table structure for table `soportes`
--

CREATE TABLE `soportes` (
  `id` int UNSIGNED NOT NULL,
  `motivo` varchar(255) NOT NULL,
  `atendido` tinyint(1) NOT NULL DEFAULT '0',
  `atendido_por` int UNSIGNED DEFAULT NULL,
  `id_personal` int UNSIGNED DEFAULT NULL,
  `id_departamento` int DEFAULT NULL,
  `fecha` timestamp NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `soportes`
--

INSERT INTO `soportes` (`id`, `motivo`, `atendido`, `atendido_por`, `id_personal`, `id_departamento`, `fecha`) VALUES
(1, 'Impresora no imprime bien', 1, NULL, NULL, 1, '2025-09-08 16:30:00'),
(2, 'Impresora no imprime bien', 1, 2, 5, 1, '2025-09-08 16:30:00'),
(3, 'Impresora no imprime bien', 1, 2, 5, 1, '2025-09-08 16:30:00');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int UNSIGNED NOT NULL,
  `username` varchar(255) NOT NULL,
  `id_rol` int UNSIGNED NOT NULL,
  `password_hash` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `username`, `id_rol`, `password_hash`) VALUES
(1, 'miquios', 1, 'algoooohasheado'),
(2, 'miquios', 1, 'algoooohasheado'),
(3, 'miquios', 1, 'algoooohasheado');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `departamentos`
--
ALTER TABLE `departamentos`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `personal`
--
ALTER TABLE `personal`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `cedula` (`cedula`);

--
-- Indexes for table `rol`
--
ALTER TABLE `rol`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `soportes`
--
ALTER TABLE `soportes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `departamentos`
--
ALTER TABLE `departamentos`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `personal`
--
ALTER TABLE `personal`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `rol`
--
ALTER TABLE `rol`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `soportes`
--
ALTER TABLE `soportes`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
