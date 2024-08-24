rule get_weather:
    output:
        "results/weather_report.txt",
    log:
        "logs/weather_report.log",
    script:
        "../scripts/get_weather/main.py"
