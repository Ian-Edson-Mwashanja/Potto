
-- 1. CREATE DATABASE
CREATE DATABASE PottoDB;
GO
-- 2. SELECT THE DATABASE
USE PottoDB;
GO
-- 3. CREATE ROAD ANOMALIES TABLE
CREATE TABLE RoadAnomalies
(
    id INT IDENTITY(1,1) PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    severity VARCHAR(20) NOT NULL,
    confidence DECIMAL(5,4) NOT NULL,
    latitude DECIMAL(10,7) NOT NULL,
    longitude DECIMAL(10,7) NOT NULL,
    detected_at DATETIME NOT NULL,
    device_id VARCHAR(50) NOT NULL
);
GO
-- 4. INSERT TEST DATA
INSERT INTO RoadAnomalies
(
    type,
    severity,
    confidence,
    latitude,
    longitude,
    detected_at,
    device_id
)
VALUES
(
    'severe_pothole',
    'severe',
    0.9453,
    -18.1235021,
    31.0568012,
    GETDATE(),
    'POTTO-001'
);
INSERT INTO RoadAnomalies
(
    type,
    severity,
    confidence,
    latitude,
    longitude,
    detected_at,
    device_id
)
VALUES
(
    'small_pothole',
    'moderate',
    0.9120,
    -18.1241000,
    31.0572000,
    GETDATE(),
    'POTTO-001'
);
INSERT INTO RoadAnomalies
(
    type,
    severity,
    confidence,
    latitude,
    longitude,
    detected_at,
    device_id
)
VALUES
(
    'rough_road',
    'moderate',
    0.8730,
    -18.1248000,
    31.0579000,
    GETDATE(),
    'POTTO-001'
);
INSERT INTO RoadAnomalies
(
    type,
    severity,
    confidence,
    latitude,
    longitude,
    detected_at,
    device_id
)
VALUES
(
    'speed_bump',
    'low',
    0.9560,
    -18.1254000,
    31.0585000,
    GETDATE(),
    'POTTO-001'
);
GO
-- 5. VIEW ALL DETECTIONS
SELECT *
FROM RoadAnomalies;
GO
-- 6. SHOW ONLY POTHOLES
SELECT *
FROM RoadAnomalies
WHERE type LIKE '%pothole%';
GO
-- 7. SHOW SEVERE ROAD PROBLEMS
SELECT *
FROM RoadAnomalies
WHERE severity = 'severe';
GO
-- 8. SHOW HIGH-CONFIDENCE DETECTIONS
SELECT *
FROM RoadAnomalies
WHERE confidence >= 0.9000;
GO
-- 9. COUNT TOTAL ANOMALIES
SELECT COUNT(*) AS total_anomalies
FROM RoadAnomalies;
GO
-- 10. COUNT ANOMALIES BY TYPE
SELECT
    type,
    COUNT(*) AS total
FROM RoadAnomalies
GROUP BY type;
GO
-- 11. COUNT ANOMALIES BY SEVERITY
SELECT
    severity,
    COUNT(*) AS total
FROM RoadAnomalies
GROUP BY severity;
GO
-- 12. SHOW NEWEST DETECTIONS FIRST
SELECT *
FROM RoadAnomalies
ORDER BY detected_at DESC;
GO
