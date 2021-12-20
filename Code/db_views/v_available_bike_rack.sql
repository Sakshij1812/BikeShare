
DROP VIEW IF EXISTS v_available_bike_rack;

CREATE VIEW v_available_bike_rack AS 
select d.*, d.rack_count - d.available_bike_count as available_rack_count from (
select a.station_id, c.station_name, c.latitude, c.longitude, a.rack_count, ifnull( b.available_bike_count, 0) as available_bike_count from (
(select id as station_id, rack_count from station s group by station_id) a 
left join
(select station_id, count(bike_id) as available_bike_count from v_bike_status vbs where
is_available = 1 
and is_rented = 0
and is_defect = 0
group by station_id) b
on a.station_id = b.station_id
left join station s
on a.station_id = s.id
) c
) d
;

select * from v_available_bike_rack 


