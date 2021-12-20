
DROP VIEW IF EXISTS v_bike_status; 

CREATE VIEW v_bike_status AS 
select bs.bike_id, b.type, b.bike_number, bs.station_id, s.station_name, s.latitude , s.longitude, s.rack_count,
bs.is_available, bs.is_defect, bs.is_rented, bs.is_temp_parked 
from bike_status bs 
left join bike b
on bs.bike_id = b.id 
left join station s 
on s.id = bs.station_id 
;

SELECT * from v_bike_status 


