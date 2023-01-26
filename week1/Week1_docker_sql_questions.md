# Question 2.Understanding docker first run

Package    Version
---------- -------
pip        22.0.4
setuptools 58.1.0
wheel      0.38.4

# Question 3. Count records

SELECT count(*)
FROM public.green_taxi_trips
WHERE date(lpep_pickup_datetime) = date('2019-01-15')
	AND date(lpep_dropoff_datetime) = date('2019-01-15')
-- 20530

# Question 4. Largest trip for each day
SELECT date(lpep_pickup_datetime)
	, trip_distance 
FROM public.green_taxi_trips
ORDER BY trip_distance DESC
limit 1;
-- 2019-01-15	117.99

# Question 5. The number of passengers
SELECT sum(CASE WHEN passenger_count=2 THEN 1 ELSE 0 end) pass_2 
, sum(CASE WHEN passenger_count=3 THEN 1 ELSE 0 end) pass_3
FROM public.green_taxi_trips
WHERE date(lpep_pickup_datetime) = date('2019-01-01')
-- pass_2	   pass_3
-- 1,282	    254
   
# Question 6. Largest tip
SELECT do_zl."Zone"  do_zone
	, tip_amount 
FROM public.green_taxi_trips gtp
LEFT JOIN public.zone_lookup pu_zl
	ON gtp."PULocationID" = pu_zl."LocationID" 
LEFT JOIN public.zone_lookup do_zl
	ON gtp."DOLocationID" = do_zl."LocationID" 
WHERE pu_zl."Zone" like 'Astoria'
ORDER BY 2 DESC
LIMIT 1
--drop_off_zone	           tip_amount
--Long Island City/Queens    Plaza	88
