<ScatterPlot
    data={query}
    x=date
    y=avg_score
    series=species__common_name
    chartAreaHeight=360
/>


-----

```sql query
  select 
      species__common_name,
      avg(score) as avg_score,
      timestamp::date as date
  from birdproject.detections
  where timestamp::date != '2024-12-05'::date
  group by 1, 3
```


