

USE WaterWatchDB;
GO

-- Table 1: Locations
CREATE TABLE Locations (
    location_id INT PRIMARY KEY IDENTITY(1,1),
    area_name VARCHAR(100),
    district VARCHAR(100),
    state VARCHAR(100)
);

-- Table 2: Water Quality Records
CREATE TABLE WaterQuality (
    record_id INT PRIMARY KEY IDENTITY(1,1),
    location_id INT FOREIGN KEY REFERENCES Locations(location_id),
    ph FLOAT,
    tds FLOAT,
    turbidity FLOAT,
    hardness FLOAT,
    status VARCHAR(20),
    test_date DATE
);

-- Table 3: Users/Admin
CREATE TABLE Users (
    user_id INT PRIMARY KEY IDENTITY(1,1),
    username VARCHAR(50),
    password VARCHAR(50),
    role VARCHAR(20)
);

-- 4 Alerts Table
CREATE TABLE Alerts (
    alert_id INT PRIMARY KEY IDENTITY(1,1),
    record_id INT FOREIGN KEY REFERENCES WaterQuality(record_id),
    message VARCHAR(200)
);
-- Sample data
INSERT INTO Locations VALUES ('Gudlavalleru','Krishna','Andhra Pradesh');

INSERT INTO Users VALUES ('admin','admin123','Admin');