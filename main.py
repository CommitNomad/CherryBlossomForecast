from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import csv

years = []
days_of_year = []

# Load cherry blossom bloom dates from CSV
with open('busan_bloom_dates.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        year = int(row['year'])
        dt = datetime.strptime(row['date'], '%Y-%m-%d') # Convert dates to day-of-year format(e.g., 2025-03-22 → 81)
        doy = dt.timetuple().tm_yday
        years.append(year)
        days_of_year.append(doy)

# Compute linear regression manually
# Using least squares method
n = len(days_of_year)
sum_x = sum(years)
sum_y = sum(days_of_year)
sum_xy = sum(y * d for y, d in zip(years, days_of_year))
sum_x2 = sum(y * y for y in years)

m = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
b = (sum_y - m * sum_x) / n

print(f"\nSlope (m): {m:.4f}")
print(f"Intercept (b): {b:.4f}")

# Predict bloom day for 2025
x_pred = 2025
y_pred = m * x_pred + b

day_of_year = round(y_pred)

# Convert DOY back to readable date
date = datetime(x_pred, 1, 1) + timedelta(days=day_of_year - 1)

# ANSI color code for magenta (pink-like)
pink = "\033[95m"
reset = "\033[0m"

# Print predicted day and date
print(f"\n🌸 Predicted Cherry Blossom Day for 2025: {day_of_year} ({pink}{date.strftime('%B %d')}{reset})\n")

# Plot historical data and regression line
plot_x = years + [x_pred]
plot_y = days_of_year + [y_pred]

regression_y = [m * x + b for x in plot_x]

plt.scatter(plot_x, plot_y, marker='o', linestyle='-', color='pink', label="Previous Years Blooms")
plt.scatter(x_pred, y_pred, color='red', edgecolors='black', s=100, label='Predicted Bloom for 2025')
plt.plot(plot_x, regression_y, color='purple', label='Regression Line')
plt.title('Cherry Blossom Forecast')
plt.xlabel('Year')
plt.ylabel('Day of Year (1 = Jan 1)')
plt.legend()
plt.grid(True)
plt.xticks(plot_x)  # Show every year on x-axis
plt.tight_layout()
plt.show()