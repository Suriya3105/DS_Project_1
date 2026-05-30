queries = {

# ---------------------------------------------------
# MAGNITUDE & DEPTH
# ---------------------------------------------------

"1. Top 10 strongest earthquakes": """

SELECT place, country, mag, depth_km, time
FROM earthquakes
ORDER BY mag DESC
LIMIT 10

""",

"2. Top 10 deepest earthquakes": """

SELECT place, country, depth_km, mag, time
FROM earthquakes
ORDER BY depth_km DESC
LIMIT 10

""",

"3. Shallow earthquakes <50km & mag >7.5": """

SELECT place, country, mag, depth_km, time
FROM earthquakes
WHERE depth_km < 50
AND mag > 7.5
ORDER BY mag DESC

""",

"4. Average depth per continent": """

SELECT country,
ROUND(AVG(depth_km),2) AS avg_depth
FROM earthquakes
GROUP BY country
ORDER BY avg_depth DESC

""",

"5. Average magnitude per magType": """

SELECT magType,
ROUND(AVG(mag),2) AS avg_mag
FROM earthquakes
GROUP BY magType
ORDER BY avg_mag DESC

""",

# ---------------------------------------------------
# TIME ANALYSIS
# ---------------------------------------------------

"6. Year with most earthquakes": """

SELECT year,
COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY year
ORDER BY total_earthquakes DESC

""",

"7. Month with highest earthquakes": """

SELECT month,
COUNT(*) AS total_earthquakes
FROM earthquakes
GROUP BY month
ORDER BY total_earthquakes DESC

""",

"8. Day of week with most earthquakes": """

SELECT day_of_week,
COUNT(*) AS total
FROM earthquakes
GROUP BY day_of_week
ORDER BY total DESC

""",

"9. Earthquakes per hour": """

SELECT hour,
COUNT(*) AS total
FROM earthquakes
GROUP BY hour
ORDER BY hour

""",

"10. Most active reporting network": """

SELECT net,
COUNT(*) AS total
FROM earthquakes
GROUP BY net
ORDER BY total DESC

""",

# ---------------------------------------------------
# CASUALTIES & ECONOMIC LOSS
# ---------------------------------------------------

"11. Top 5 significant earthquakes": """

SELECT place,
country,
sig,
mag
FROM earthquakes
ORDER BY sig DESC
LIMIT 5

""",

"12. Total significance per country": """

SELECT country,
SUM(sig) AS total_significance
FROM earthquakes
GROUP BY country
ORDER BY total_significance DESC

""",

"13. Average significance by alert level": """

SELECT alert,
ROUND(AVG(sig),2) AS avg_significance
FROM earthquakes
GROUP BY alert

""",

# ---------------------------------------------------
# EVENT TYPE & QUALITY METRICS
# ---------------------------------------------------

"14. Reviewed vs automatic earthquakes": """

SELECT status,
COUNT(*) AS total
FROM earthquakes
GROUP BY status

""",

"15. Count by earthquake type": """

SELECT type,
COUNT(*) AS total
FROM earthquakes
GROUP BY type

""",

"16. Number by data type": """

SELECT types,
COUNT(*) AS total
FROM earthquakes
GROUP BY types
ORDER BY total DESC

""",

"17. Average RMS & GAP per continent": """

SELECT country,
ROUND(AVG(rms),2) AS avg_rms,
ROUND(AVG(gap),2) AS avg_gap
FROM earthquakes
GROUP BY country

""",

"18. High station coverage events": """

SELECT place,
country,
mag,
nst
FROM earthquakes
WHERE nst > 100
ORDER BY nst DESC

""",

# ---------------------------------------------------
# TSUNAMI & ALERTS
# ---------------------------------------------------

"19. Tsunami events per year": """

SELECT year,
COUNT(*) AS tsunami_events
FROM earthquakes
WHERE tsunami = 1
GROUP BY year
ORDER BY year

""",

"20. Earthquakes by alert level": """

SELECT alert,
COUNT(*) AS total
FROM earthquakes
GROUP BY alert

""",

# ---------------------------------------------------
# SEISMIC PATTERNS & TRENDS
# ---------------------------------------------------

"21. Top 5 countries by avg magnitude": """

SELECT country,
ROUND(AVG(mag),2) AS avg_mag
FROM earthquakes
GROUP BY country
ORDER BY avg_mag DESC
LIMIT 5

""",

"22. Countries with shallow & deep earthquakes": """

SELECT country,
year,
month
FROM earthquakes
GROUP BY country, year, month
HAVING
SUM(depth_category='Shallow') > 0
AND
SUM(depth_category='Deep') > 0

""",

"23. Year-over-year growth rate": """

WITH yearly AS (

SELECT year,
COUNT(*) AS total_eq
FROM earthquakes
GROUP BY year

)

SELECT year,
total_eq,
LAG(total_eq) OVER(ORDER BY year) AS prev_year,

ROUND(
(
(total_eq - LAG(total_eq)
OVER(ORDER BY year))
/
LAG(total_eq)
OVER(ORDER BY year)
) * 100,
2
) AS growth_rate

FROM yearly

""",

"24. Top 3 seismically active regions": """

SELECT country,
COUNT(*) AS frequency,
ROUND(AVG(mag),2) AS avg_mag,

ROUND(
COUNT(*) * AVG(mag),
2
) AS seismic_score

FROM earthquakes
GROUP BY country
ORDER BY seismic_score DESC
LIMIT 3

""",

# ---------------------------------------------------
# DEPTH & LOCATION ANALYSIS
# ---------------------------------------------------

"25. Avg depth near equator": """

SELECT country,
ROUND(AVG(depth_km),2) AS avg_depth
FROM earthquakes
WHERE latitude BETWEEN -5 AND 5
GROUP BY country
ORDER BY avg_depth DESC

""",

"26. Highest shallow/deep ratio": """

SELECT country,

SUM(depth_category='Shallow') AS shallow_count,

SUM(depth_category='Deep') AS deep_count,

ROUND(
SUM(depth_category='Shallow')
/
NULLIF(SUM(depth_category='Deep'),0),
2
) AS ratio

FROM earthquakes
GROUP BY country
ORDER BY ratio DESC

""",

"27. Avg magnitude tsunami vs non-tsunami": """

SELECT tsunami,
ROUND(AVG(mag),2) AS avg_mag
FROM earthquakes
GROUP BY tsunami

""",

"28. Lowest reliability events": """

SELECT place,
country,
rms,
gap,

ROUND(
(rms + gap)/2,
2
) AS reliability_score

FROM earthquakes
ORDER BY reliability_score DESC
LIMIT 20

""",

"29. Consecutive earthquakes": """

WITH ordered_eq AS (

SELECT *,

LEAD(time) OVER(ORDER BY time) AS next_time,

LEAD(place) OVER(ORDER BY time) AS next_place

FROM earthquakes

)

SELECT place,
next_place,
time,
next_time

FROM ordered_eq

WHERE TIMESTAMPDIFF(HOUR, time, next_time) <= 1

""",

"30. Deep-focus earthquake regions": """

SELECT country,
COUNT(*) AS deep_focus_events
FROM earthquakes
WHERE depth_km > 300
GROUP BY country
ORDER BY deep_focus_events DESC

"""

}