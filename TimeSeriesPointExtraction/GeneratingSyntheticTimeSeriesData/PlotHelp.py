import matplotlib.pyplot as plt

def plot_time_series(time, values, label='Time Series'):
    plt.figure(figsize=(10,6))
    plt.plot(time, values)
    plt.xlabel("Time", fontsize=20)
    plt.ylabel("Value", fontsize=20)
    plt.title(label, fontsize=20)
    plt.grid(True)
	
def plot_bar_graph(data_keys, data_values, color='blue', label='Bar Plot', xlabel='Keys'):
	plt.bar(data_keys, data_values, color = color,  width = 0.4) 
	plt.xlabel(xlabel) 
	plt.ylabel("Number") 
	plt.title(label) 
	
def plot_line_chart(x_data, y_data, color='blue', label='Line Plot', xlabel='X Axis', ylabel='Y Axis'):
	plt.plot(xAxis,yAxis, color=color)
	plt.title(label)
	plt.xlabel(xlabel)
	plt.ylabel(ylabel)
