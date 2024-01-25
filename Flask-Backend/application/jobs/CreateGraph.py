import os
import matplotlib.pyplot as plt

def linegraph(data):
    # Sample data for the first plot
    x1 = [1, 2, 3, 4, 5]
    y1 = [2, 3, 5, 7, 11]

    # Create the first plot
    plt.figure()  # Create a new figure
    plt.plot(x1, y1)
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.title('First Plot')
    plt.savefig('first_plot.png')

def pieChart(data, title):
    # Sample data for the second plot (Pie chart)
    labels = list(data.keys())
    sizes = list(data.values())  # Sizes in percentage

    # Create the second plot (Pie chart)
    plt.figure()  # Create a new figure
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title(title)
    count = len(os.listdir('./PDF_Report/'))
    piename = f'./PDF_Report/pie_{count}.png'
    plt.savefig(piename)
    return piename

# Show the plots (optional)
# plt.show()
