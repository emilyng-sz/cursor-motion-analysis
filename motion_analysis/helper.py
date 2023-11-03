# define helper functions for motion_analysis purposes

def round_to_factor(number, factor):
    return ((number + factor // 2) // factor ) * factor

def orientation(p, q, r):
    '''
    Given three points p, q, and r, calculate the orientation of the vectors (p,q) and (q,r)
    '''
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0  # Collinear
    return 1 if val > 0 else -1  # Clockwise or Counterclockwise

def is_clockwise_or_counterclockwise(polygon):
    ''' Given a list of points, check if the points form either a clockwise or counterclockwise loop.
    '''
    n = len(polygon)
    if n < 5:
        return False  # A polygon must have at least 5 points
    
    orientation_sum = 0
    for i in range(n):
        orientation_sum += orientation(polygon[i], polygon[(i + 1) % n], polygon[(i + 2) % n])

    return int(0.8*n) <= abs(orientation_sum)


# --- functions for analysing analysis results --- #

def get_all_info(all_info, time_coord_data):
    all_info_dct = [] # key value pairs of start_time: info
    for info in all_info:
        all_info_dct.append(get_info(info[0], info[1], info[2], time_coord_data))
    return all_info_dct

def get_info(start_time, end_time, type, time_coord_data):
    '''
    takes in a start and end time and returns a dictionary with information stored, depending on type
    '''
    info = {}
    info['start_time'] = start_time
    info['end_time'] = end_time
    info['type'] = type
    coord_data = list(map(lambda x: x[1], filter(lambda tup: tup[0] >= start_time and tup[0] <= end_time, time_coord_data)))

    if type == 'loop':
        info['start_pos'] = coord_data[0]
        info['end_pos'] = coord_data[-1]
        bbox = get_bounding_box(coord_data)
        info['bounding_box'] = bbox
        info['center'] = ((bbox['max_x'] - bbox['min_x'])//2, (bbox['max_y'] - bbox['min_y'])//2)
    
    if type == 'stationary':
        info['pos'] = (sum(map(lambda x: x[0], coord_data))//len(coord_data), sum(map(lambda x: x[1], coord_data))//len(coord_data))
    
    if type == 'underline':
        info['start_pos'] = coord_data[0]
        info['end_pos'] = coord_data[-1]
        info['max_distance'] = round(max(coord_data, key=lambda p: p[0])[0] - min(coord_data, key=lambda p: p[0])[0])
        
    return info

def get_bounding_box(points):
    '''
    takes in a list of coordinates and returns a dictionary with the bounding box
    '''
    min_x = min(points, key=lambda p: p[0])[0]
    max_x = max(points, key=lambda p: p[0])[0]
    min_y = min(points, key=lambda p: p[1])[1]
    max_y = max(points, key=lambda p: p[1])[1]

    bounding_box = {
        'min_x': min_x,
        'max_x': max_x,
        'min_y': min_y,
        'max_y': max_y
    }

    return bounding_box