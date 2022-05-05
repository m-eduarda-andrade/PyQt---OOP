# Fehlerbehandlung


data = ["hey", "you"]

try:
    print(data[2])
except (ValueError, IndexError):
    print("ops")



data = {"1": "spam", "2": "bacon", "3": "eggs"}
print(data)
print(sorted(data.items(), key=lambda item: item[1][-1]))
