import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Define metrics
    manual_time = 4.5  # Average time spent manually (hours)
    automated_time = 0.5  # Time spent with automation (hours)
    hourly_rate = 25  # Cost per hour ($)

    # Calculate savings
    time_saved = manual_time - automated_time
    manual_cost = manual_time * hourly_rate
    automated_cost = automated_time * hourly_rate
    cost_saved = manual_cost - automated_cost

    categories = ["Manual Process", "Automated Process"]
    time_spent = [manual_time, automated_time]
    costs = [manual_cost, automated_cost]

    # Create a bar chart for time spent
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.bar(categories, time_spent, color=['red', 'green'])
    plt.title("Time Spent (Hours)")
    plt.ylabel("Hours")
    plt.ylim(0, 5)
    plt.grid(axis='y')

    # Create a bar chart for costs
    plt.subplot(1, 2, 2)
    plt.bar(categories, costs, color=['red', 'green'])
    plt.title("Cost ($)")
    plt.ylabel("Dollars")
    plt.ylim(0, max(costs) + 20)  # Adjust y-limit based on max cost
    plt.grid(axis='y')

    plt.tight_layout()
    plt.savefig("output_data/savings_visualization.png")
    plt.show()
    print("Savings visualization saved.")

if __name__ == "__main__":
    main()
