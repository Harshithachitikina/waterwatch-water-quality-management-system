INSERT INTO Users VALUES ('admin','admin123','Admin');
INSERT INTO Users VALUES ('officer1','water123','Officer');

INSERT INTO Locations VALUES ('Gudlavalleru','Krishna','Andhra Pradesh');
INSERT INTO Locations VALUES ('Vijayawada','NTR','Andhra Pradesh');
INSERT INTO Locations VALUES ('Machilipatnam','Krishna','Andhra Pradesh');
INSERT INTO Locations VALUES ('Rajamundry','East Godavari','Andhra Pradesh');
INSERT INTO Locations VALUES ('Bhimavaram','West Godavari','Andhra Pradesh');

INSERT INTO WaterQuality VALUES (1,7.2,320,3,180,'Safe','2026-03-10');
INSERT INTO WaterQuality VALUES (2,8.9,650,7,350,'Unsafe','2026-03-11');
INSERT INTO WaterQuality VALUES (3,7.0,400,4,200,'Safe','2026-03-12');
INSERT INTO WaterQuality VALUES (4,6.2,550,6,310,'Unsafe','2026-03-13');
INSERT INTO WaterQuality VALUES (5,7.5,280,2,150,'Safe','2026-03-14');
INSERT INTO Alerts VALUES (2,'Unsafe water detected');
INSERT INTO Alerts VALUES (4,'Unsafe water detected');



INSERT INTO Users VALUES ('analyst1','data123','Analyst');
select * from WaterQuality;
