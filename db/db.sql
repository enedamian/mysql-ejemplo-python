DROP DATABASE IF EXISTS tienda_ejemplo_python;
CREATE DATABASE tienda_ejemplo_python;

USE tienda_ejemplo_python;

-- Base simplificada para mostrar operaciones CRUD en productos
-- desde una API REST con Python y MySQL.

CREATE TABLE `productos` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `nombre` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `stock` int NOT NULL DEFAULT '0',
  CONSTRAINT `productos_chk_1` CHECK (`precio` >= 0),
  CONSTRAINT `productos_chk_2` CHECK (`stock` >= 0)
) ;


-- Algunos inserts de ejemplo para tener datos cargados inicialmente.

INSERT INTO `productos` (`nombre`, `precio`, `descripcion`, `stock`) VALUES
('AMD Ryzen 5 5600X', 199.99, 'Procesador de 6 núcleos y 12 hilos con arquitectura Zen 3.', 15),
('Intel Core i7-11700K', 349.99, 'Procesador de 8 núcleos y 16 hilos con arquitectura Rocket Lake.', 10),
('NVIDIA GeForce RTX 3060', 399.99, 'Tarjeta gráfica con arquitectura Ampere y 12GB de memoria GDDR6.', 8),
('Corsair Vengeance LPX 16GB (2 x 8GB) DDR4-3200', 89.99, 'Kit de memoria RAM de alto rendimiento para gaming y multitarea.', 25),
('Samsung 970 EVO Plus 1TB NVMe SSD', 149.99, 'Unidad de estado sólido NVMe con velocidades de lectura/escritura rápidas.', 20),
('ASUS ROG Strix B550-F Gaming', 179.99, 'Placa base ATX con chipset B550 para procesadores AMD Ryzen.', 12),
('Cooler Master Hyper 212 Black Edition', 39.99, 'Disipador de CPU con ventilador de 120mm para una refrigeración eficiente.', 30),
('Seagate BarraCuda 2TB HDD', 54.99, 'Disco duro interno de 2TB con velocidad de 7200 RPM para almacenamiento masivo.', 18);