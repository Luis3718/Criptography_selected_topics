-- Crear la base de datos
CREATE DATABASE Tienda;
USE Tienda;

-- Crear la tabla Customers (Clientes) con datos personales y de login
CREATE TABLE Customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    FullName VARCHAR(255) NOT NULL,
    PhoneNumber VARCHAR(15) NOT NULL,
    CreditCardNumber VARCHAR(255) NOT NULL, -- Este campo debe estar encriptado en la aplicación
    Username VARCHAR(255) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL, -- Almacenar contraseñas de manera segura (hash)
    Salt VARCHAR(32) NOT NULL
);

-- Crear la tabla Employees (Empleados) con datos personales, de login y llave pública de ECDSA
CREATE TABLE Employees (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    FullName VARCHAR(255) NOT NULL,
    Username VARCHAR(255) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL, -- Almacenar contraseñas de manera segura (hash)
    PublicKeyECDSA TEXT NOT NULL, -- Almacenar la llave pública de ECDSA en formato PEM o similar
    Salt VARCHAR(32) NOT NULL
);

-- Crear la tabla AdminUsers (Administradores) independiente
CREATE TABLE AdminUsers (
    AdminID INT AUTO_INCREMENT PRIMARY KEY,
    FullName VARCHAR(255) NOT NULL,
    Username VARCHAR(255) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL -- Almacenar contraseñas de manera segura (hash)
);

-- Crear la tabla Products (Productos)
CREATE TABLE Products (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    ProductName VARCHAR(255) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL
);

-- Crear la tabla Transactions (Transacciones)
CREATE TABLE Transactions (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    EmployeeID INT NOT NULL,
    DateOfSale DATETIME DEFAULT CURRENT_TIMESTAMP,
    TotalAmount DECIMAL(10, 2) NOT NULL,
    CreditCardNumber VARCHAR(255) NOT NULL, -- Este campo debe estar encriptado en la aplicación
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
);

-- Crear la tabla TransactionDetails (Detalles de Transacciones)
CREATE TABLE TransactionDetails (
    TransactionDetailID INT AUTO_INCREMENT PRIMARY KEY,
    TransactionID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    FOREIGN KEY (TransactionID) REFERENCES Transactions(TransactionID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- Crear la tabla MonthlySalesReports (Reportes de Ventas Mensuales)
CREATE TABLE MonthlySalesReports (
    ReportID INT AUTO_INCREMENT PRIMARY KEY,
    EmployeeID INT NOT NULL,
    Month VARCHAR(7) NOT NULL, -- Formato: YYYY-MM
    TotalSales DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
);

-- Datos para poblar la base de datos
INSERT INTO Products (ProductName, Price)
VALUES ('Playera verde', 200.00), 
       ('Playera roja', 200.00),
       ('Playera gris', 200.00),
       ('Playera cafe', 200.00),
       ('Playera azul', 200.00),
       ('Pantalon azul', 250.00),
       ('Pantalon gris', 250.00),
       ('Playera negro', 250.00),
       ('Cartera', 100.00);

-- Transacciones para cada cliente y empleado
INSERT INTO Transactions (CustomerID, EmployeeID, DateOfSale, TotalAmount, CreditCardNumber)
VALUES
-- Cliente 1 con empleado 1
(1, 1, '2024-09-15 10:30:00', 450.00, '8721089747658897'),
(1, 1, '2024-10-01 14:20:00', 550.00, '8721089747658897'),
(1, 1, '2024-11-05 17:45:00', 350.00, '8721089747658897'),

-- Cliente 2 con empleado 2
(2, 2, '2024-09-20 11:00:00', 650.00, '3739168195182335'),
(2, 2, '2024-10-15 13:10:00', 750.00, '3739168195182335'),
(2, 2, '2024-11-10 15:30:00', 850.00, '3739168195182335'),

-- Cliente 3 con empleado 1
(3, 1, '2024-09-25 12:00:00', 450.00, '4648139926467678'),
(3, 1, '2024-10-05 16:00:00', 550.00, '4648139926467678'),
(3, 1, '2024-11-20 18:30:00', 650.00, '4648139926467678');


-- Detalles de transacciones para cada transacción
INSERT INTO TransactionDetails (TransactionID, ProductID, Quantity)
VALUES
-- Detalles para la primera transacción
(1, 1, 2), -- Playera verde x2
(1, 6, 1), -- Pantalón azul x1

-- Detalles para la segunda transacción
(2, 2, 1), -- Playera roja x1
(2, 7, 2), -- Pantalón gris x2

-- Detalles para la tercera transacción
(3, 4, 3), -- Playera café x3

-- Detalles para la cuarta transacción
(4, 5, 1), -- Playera azul x1
(4, 8, 1), -- Playera negra x1

-- Detalles para la quinta transacción
(5, 3, 2), -- Playera gris x2
(5, 9, 2), -- Cartera x2

-- Detalles para la sexta transacción
(6, 6, 3), -- Pantalón azul x3

-- Detalles para la séptima transacción
(7, 2, 1), -- Playera roja x1
(7, 3, 1), -- Playera gris x1
(7, 8, 1), -- Playera negra x1

-- Detalles para la octava transacción
(8, 4, 2), -- Playera café x2
(8, 7, 1), -- Pantalón gris x1

-- Detalles para la novena transacción
(9, 1, 3), -- Playera verde x3
(9, 5, 1); -- Playera azul x1
