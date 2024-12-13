<ScatterPlot
    data={query}
    x=date
    y=probability
    series=species__common_name
    yFmt="pct0"
    chartAreaHeight=360
/>


-----

```sql query
  select 
      id,
      species__common_name,
      species__scientific_name,
      probability,
      timestamp::date as date
  from birdproject.detections
  where timestamp::date != '2024-12-05'::date
```


