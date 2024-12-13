<ScatterPlot
    data={query}
    y=probability
    x=cnt
    yFmt="pct0"
    xMax="100"
    xMin="0"
    pointSize="5"
    chartAreaHeight=720
    series=species__common_name
/>


-----

```sql query
  select 
      species__common_name,
      probability,
      count(*) as cnt,
      timestamp::date as date
  from birdproject.detections
  where timestamp::date != '2024-12-05'::date
  group by 1,2,4
```


