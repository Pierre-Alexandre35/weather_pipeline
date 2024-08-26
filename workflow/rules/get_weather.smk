rule get_weather:
    output:
        "results/weather_report.txt",
    log:
        "logs/weather_report.log",
    params:
        longitude=config["longitude"],
        latitude=config["latitude"],
        forecast_days=config.get("forecast_days", None)
    script:
        "../scripts/get_weather/main.py"
