create database Tienda;
use Tienda;

-- Create the Customers table
CREATE TABLE Customers (
    CustomerID INT AUTO_INCREMENT PRIMARY KEY,
    FullName VARCHAR(255) NOT NULL,
    PhoneNumber VARCHAR(15) NOT NULL,
    CreditCardNumber VARCHAR(255) NOT NULL -- Encrypt this field in the application
);

-- Create the Products table
CREATE TABLE Products (
    ProductID INT AUTO_INCREMENT PRIMARY KEY,
    ProductName VARCHAR(255) NOT NULL,
    Price DECIMAL(10, 2) NOT NULL
);

-- Create the Employees table
CREATE TABLE Employees (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    FullName VARCHAR(255) NOT NULL
);

-- Create the CustomerUsers table
CREATE TABLE CustomerUsers (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    Username VARCHAR(255) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL, -- Store securely hashed passwords
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID) ON DELETE CASCADE
);

-- Create the EmployeeUsers table
CREATE TABLE EmployeeUsers (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    EmployeeID INT NOT NULL,
    Username VARCHAR(255) UNIQUE NOT NULL,
    PasswordHash VARCHAR(255) NOT NULL, -- Store securely hashed passwords
    Role ENUM('Employee', 'Admin') NOT NULL, -- Admin or regular employee
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID) ON DELETE CASCADE
);

-- Create the Transactions table
CREATE TABLE Transactions (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    CustomerID INT NOT NULL,
    EmployeeID INT NOT NULL,
    DateOfSale DATETIME DEFAULT CURRENT_TIMESTAMP,
    TotalAmount DECIMAL(10, 2) NOT NULL,
    CreditCardNumber VARCHAR(255) NOT NULL, -- Encrypt this field in the application
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
);

-- Create the TransactionDetails table
CREATE TABLE TransactionDetails (
    TransactionDetailID INT AUTO_INCREMENT PRIMARY KEY,
    TransactionID INT NOT NULL,
    ProductID INT NOT NULL,
    Quantity INT NOT NULL,
    FOREIGN KEY (TransactionID) REFERENCES Transactions(TransactionID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

-- Create the MonthlySalesReports table
CREATE TABLE MonthlySalesReports (
    ReportID INT AUTO_INCREMENT PRIMARY KEY,
    EmployeeID INT NOT NULL,
    Month VARCHAR(7) NOT NULL, -- Format: YYYY-MM
    TotalSales DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
);

-- Insert sample data for Customers
INSERT INTO Customers (FullName, PhoneNumber, CreditCardNumber)
VALUES ('Luis Alvarado', '5555451234', '45265186356125796'),
       ('Pedro Insunza', '555558678', '4564823647526476'),
       ('Benja ortega', '556825678', '4591688615364875'),
       ('Jesus Ramirez', '5568654458', '4596588455364875'),
       ('Orlando Juarez', '5568687458', '4596289655364875'),

-- Insert sample data for Products
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


-- Insert sample data for Employees
INSERT INTO Employees (FullName)
VALUES ('Alice Johnson'),
       ('Bob Brown'),
       ('Charlie Davis'),
       ('Diana Evans'),
       ('Evan Fox');

-- Insert sample data for CustomerUsers
INSERT INTO CustomerUsers (CustomerID, Username, PasswordHash)
VALUES 
    (1, 'john_doe', 'hashed_password_1'), -- Customer linked to CustomerID 1
    (2, 'jane_smith', 'hashed_password_2'); -- Customer linked to CustomerID 2

-- Insert sample data for EmployeeUsers
INSERT INTO EmployeeUsers (EmployeeID, Username, PasswordHash, Role)
VALUES 
    (1, 'alice', 'hashed_password_3', 'Employee'), -- Employee linked to EmployeeID 1
    (2, 'bob', 'hashed_password_4', 'Employee'), -- Employee linked to EmployeeID 2
    (3, 'admin', 'hashed_password_5', 'Admin'); -- Admin linked to EmployeeID 3

-- Insert a sample transaction
INSERT INTO Transactions (CustomerID, EmployeeID, TotalAmount, CreditCardNumber)
VALUES (1, 1, 70.00, 'encrypted_card_1');

-- Insert transaction details
INSERT INTO TransactionDetails (TransactionID, ProductID, Quantity)
VALUES (1, 1, 2), -- 2 T-Shirts
       (1, 2, 1); -- 1 Pair of Jeans

-- Insert a sample monthly sales report
INSERT INTO MonthlySalesReports (EmployeeID, Month, TotalSales)
VALUES (1, '2024-11', 70.00);
