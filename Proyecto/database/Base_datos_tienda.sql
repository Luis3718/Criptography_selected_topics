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

