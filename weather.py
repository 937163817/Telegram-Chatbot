from weather import Weather, Unit

weather = Weather(unit=Unit.CELSIUS)

lookup = weather.lookup(560743)
condition = lookup.condition

print(condition.text)

weather = Weather(unit=Unit.CELSIUS)

location = weather.lookup_by_location('dublin')
forecasts = location.forecast
for forecast in forecasts:
    print(forecast.text)
    print(forecast.date)
    print(forecast.high)
    print(forecast.low)
	
weather = Weather(Unit.CELSIUS)
lookup = w.lookup_by_latlng(53.3494,-6.2601)
condition = lookup.condition
print(condition.text)