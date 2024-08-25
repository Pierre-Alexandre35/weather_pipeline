rule get_weather:
    output:
        "results/weather_report.txt",
    log:
        "logs/weather_report.log",
    params:
        latitude=config["latitude"],
        longitude=config["longitude"],
    script:
        "../scripts/get_weather/main.py"
