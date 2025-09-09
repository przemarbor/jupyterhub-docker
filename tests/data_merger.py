import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

# Load data from the corrected CSV files
metrics_df = pd.read_csv('metrics.csv')
metrics_df['timestamp'] = pd.to_datetime(metrics_df['timestamp'])
tests_df = pd.read_csv('execution_times.csv')
tests_df['Timestamp'] = pd.to_datetime(tests_df['Timestamp'])

# Find all test periods
test_periods = []
current_test_id = None
start_time = None
end_time = None

for _, row in tests_df.iterrows():
    if row['Event Type'] == 'start' and current_test_id is None:
        current_test_id = row['Test ID']
        start_time = row['Timestamp']
    elif row['Event Type'] == 'TEST_COMPLETED' and current_test_id is not None:
        end_time = row['Timestamp']
        test_periods.append((current_test_id, start_time, end_time))
        current_test_id = None
        start_time = None
        end_time = None

# Prepare data for the chart - average usage per second
max_duration = 0
all_cpu_data = []
all_mem_data = []

for test_id, start, end in test_periods:
    # Get metrics for this test period
    test_metrics = metrics_df[(metrics_df['timestamp'] >= start) &
                              (metrics_df['timestamp'] <= end)].copy()
    
    # Calculate time in seconds from the start of the test
    test_metrics['seconds'] = (test_metrics['timestamp'] - start).dt.total_seconds()
    
    # Round seconds to whole values
    test_metrics['seconds'] = test_metrics['seconds'].round().astype(int)
    
    # Find the maximum test duration
    duration = test_metrics['seconds'].max()
    if duration > max_duration:
        max_duration = duration
    
    # Prepare data for aggregation
    cpu_data = test_metrics.groupby('seconds')['cpu_percent'].mean()
    mem_data = test_metrics.groupby('seconds')['mem_percent'].mean()
    
    all_cpu_data.append(cpu_data)
    all_mem_data.append(mem_data)

# Create a DataFrame with average values for each second
seconds_range = range(0, max_duration + 1)
avg_cpu = pd.DataFrame(index=seconds_range)
avg_mem = pd.DataFrame(index=seconds_range)

for i, (cpu, mem) in enumerate(zip(all_cpu_data, all_mem_data)):
    avg_cpu[f'test_{i}'] = cpu
    avg_mem[f'test_{i}'] = mem

avg_cpu['mean'] = avg_cpu.mean(axis=1)
avg_mem['mean'] = avg_mem.mean(axis=1)

# Prepare data on script execution times
results_df = tests_df[tests_df['Event Type'] == 'results'].copy()
for col in ['Time 1', 'Time 2', 'Time 3']:
    if col in results_df.columns:  # Check if column exists
        results_df[col] = results_df[col].str.replace('s', '', regex=False).astype(float)

avg_time1 = results_df['Time 1'].mean()
avg_time2 = results_df['Time 2'].mean()
avg_time3 = results_df['Time 3'].mean()

# Create charts
plt.figure(figsize=(15, 10))

# Chart 1: Average CPU and RAM usage during tests
plt.subplot(2, 1, 1)
plt.plot(avg_cpu.index, avg_cpu['mean'], label='CPU %', color='blue')
plt.plot(avg_mem.index, avg_mem['mean'], label='RAM %', color='green')
plt.xlabel('Time from test start (s)')
plt.ylabel('Percentage usage')
plt.title('Average CPU and RAM usage during tests')
plt.legend()
plt.grid(True)

# Chart 2: Average script execution times
plt.subplot(2, 1, 2)
times = [avg_time1, avg_time2, avg_time3]
labels = ['Script 1', 'Script 2', 'Script 3']
bars = plt.bar(labels, times, color=['red', 'green', 'blue'])
plt.xlabel('Script')
plt.ylabel('Time (s)')
plt.title('Average execution time for individual scripts')
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
              f'{height:.2f}s',
              ha='center', va='bottom')
plt.grid(True)

plt.tight_layout()
plt.show()

# Display statistics
print(f"Number of test runs analyzed: {len(test_periods)}")
print(f"Maximum test duration: {max_duration}s")
print(f"Average CPU usage during tests: {avg_cpu['mean'].mean():.1f}%")
print(f"Average RAM usage during tests: {avg_mem['mean'].mean():.1f}%")
print("\nAverage script execution times:")
print(f"Script 1: {avg_time1:.2f}s")
print(f"Script 2: {avg_time2:.2f}s")
print(f"Script 3: {avg_time3:.2f}s")
