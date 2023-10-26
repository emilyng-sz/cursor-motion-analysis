# define helper functions for motion_analysis purposes

## Simplify data
def get_time_x_y(all_data, height):
    ''' takes in all_data consisiting of lists of tuples (<time>, <coordinates x,y>) 
        and returns time, x and y as three separate lists
    '''
    return list(map(lambda x: x[0], all_data)), \
           list(map(lambda x: x[1][0], all_data)), \
           list(map(lambda x: height - x[1][1], all_data))

def group_coordinates(all_data, height, width, factor):
    ''' takes in all_data 
        and returns new_all_data, x and y as three separate lists '''
    return list(map(lambda tup: (tup[0], (tup[1][0]//factor, tup[1][1]//factor)), all_data)), height/factor, width/factor


## Visualise data
def plot_2D(x_values, y_values, height, width):
    ''' Visualise 2D trajectory as plot '''
    import matplotlib.pyplot as plt

    plt.scatter(x_values, y_values, color='blue', marker='o', alpha = 0.5)
    # Set axis labels and plot title
    plt.xlabel('X position')
    plt.ylabel('Y position')
    plt.title('Positions of cursor on screen')
    plt.xlim(0, width)  # Adjust the x-axis limit
    plt.ylim(0, height)
    # Display the plot
    plt.grid(True)
    plt.show()

def plot_3D(x_values, y_values, timestamps):

    ''' plot 3D plot to show position over time'''
    import matplotlib.pyplot as plt

    ax = plt.figure().add_subplot(projection='3d')

    ax.scatter(x_values, timestamps, y_values, label='Position of cursor over time')
    ## notice a scatter plot is used because there are missing timestamps in cursor detection

    ax.set_xlabel("X position")
    ax.set_ylabel("Time (ms)")
    ax.set_zlabel("Y position")
    ax.legend()

    plt.show()

def plot_3D_animation(x_values, y_values, timestamps, height, width, path):
    ''' Creates 3D plot with animation and SAVES to gif format '''
    from matplotlib import pyplot as plt
    import numpy as np
    from matplotlib import animation

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    def gen(N):
        '''return (x,y,z) in array format '''
        for i in range(N):
            yield np.array([x_values[i], timestamps[i], y_values[i]])

    def update(num, data, line):
        line.set_data(data[:2, :num])
        line.set_3d_properties(data[2, :num])

    N = len(x_values)
    data = np.array(list(gen(N))).T
    line, = ax.plot(data[0, 0:1], data[1, 0:1], data[2, 0:1])

    # Setting the axes properties
    ax.set_xlim3d([0, width])
    ax.set_xlabel('X Position')

    ax.set_ylim3d([0, timestamps[-1]])
    ax.set_ylabel('Time (ms)')

    ax.set_zlim3d([0, height])
    ax.set_zlabel('Y Position')

    ani = animation.FuncAnimation(fig, update, N, fargs=(data, line), interval=10000/N, blit=False)
    ani.save(path)
    plt.show()


