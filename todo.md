- reformat the config.yaml like this following example: 
```
cities:
  paris:
    latitude: 48.8566
    longitude: 2.3522
    forecast_days: 3
  san_francisco:
    latitude: 37.7749
    longitude: -122.4194
    forecast_days: 3
  new_york:
    latitude: 40.7128
    longitude: -74.0060
    forecast_days: 3
```
- add a new Snakefile command to be able to generate get_weather for all cities available within the config.yaml file
- be able to run Snakefile get_weather for 1 or more cities using CLI such as snakemake ```--forceall san_francisco```
- store the output in a different format (csv? parquet?)
- Use the medallion architecture (bronze, silver, gold):
  - store raw files in GCS 
  - insert enriched files into a database (PSQL?)
  - Gold = weather predictions? by using third-party libraries and current data?
- unit testing 
