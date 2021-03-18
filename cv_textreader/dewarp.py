# Page Dewarper from the Half Baked Maker
import numpy as np
#section 1 goes here


#section 2-boundary estimation, borrowed from Jupiter
def left_right_boundary_estimation(points):
    CONSTANT_Ta = 10  #threshold for removing tab lines
    valid = False
    a = -1
    b = -1
    curPoints = points.copy()

    while(not valid):
        #use OLS to find line that approximates the points
        #https://en.wikipedia.org/wiki/Ordinary_least_squares#Simple_linear_regression_model
        sumX = 0
        sumY = 0
        sumXY = 0
        sumYY = 0
        for x,y in curPoints:
            sumX += x
            sumY += y
            sumXY += x*y
            sumYY += y*y
        b = (sumXY - sumX*sumY/len(curPoints))/(sumYY-sumY*sumY/len(curPoints))
        a = sumX/len(curPoints) - b*sumY/len(curPoints)

        #remove points that are too far from the line
        valid = True
        if(b == 0):
            #flat line corner case (to avoid division by 0)
            for x,y in curPoints:
                if(abs(x - a) > CONSTANT_Ta):
                    print("removed ({},{})".format(x,y))
                    curPoints.remove((x,y))
                    valid = False
        else:
            for x,y in curPoints:
                if(abs(-a*x+y+b)/math.sqrt(a**2+1) > CONSTANT_Ta):
                    print("removed ({},{})".format(x,y))
                    curPoints.remove((x,y))
                    valid = False

    return a, b


#section 3
# Determining parameters for keystone equations
# input: (a, b) of left margin, (a, b) of right margin, height of the image
# output: np array [a0, a1, a2, a3] for transform equations

def determine_keystone_params(left_margin, right_margin, h):
    a_left, b_left = left_margin
    a_right, b_right = right_margin
    x_tl, y_tl = (b_left, 0)
    x_tr, y_tr = (b_right, 0)
    x_bl, y_bl = (a_left * h + b_left, h)
    x_br, y_br = (a_right * h + b_right, h)
    x_prime_tl = 0
    x_prime_tr = 0
    x_prime_bl = 0
    x_prime_br = 0
    if (x_tr - x_tl) >= (x_br-x_bl):
        x_prime_tl = x_tl
        x_prime_tr = x_tr
        x_prime_bl = x_tl
        x_prime_br = x_tr
    else:
        x_prime_tl = x_bl
        x_prime_tr = x_br
        x_prime_bl = x_bl
        x_prime_br = x_br

    transform_matrix = np.array([1, x_prime_tl, y_tl, x_prime_tl * y_tl],
                                [1, x_prime_tr, y_tr, x_prime_tr * y_tr],
                                [1, x_prime_bl, y_bl, x_prime_bl * y_bl],
                                [1, x_prime_br, y_br, x_prime_br * y_br])

    x_matrix = np.vstack(np.array([x_tl, x_tr, x_bl, x_br]))

    a = np.dot(np.transpose(transform_matrix), x_matrix)
    return a


# performs forward transform
# input: x point, y point, parameter array a
# output: x'
def forward_transform(x, y, a):
    x_prime = (x - a[0] - a[2]*y)/(a[1] + a[3]*y)
    return x_prime

# performs reverse transform
# input: x', y point, parameter array a
# output: x
def reverse_transform(x_prime, y, a):
    x = a[0] + a[1] * x_prime + a[2] * y + a[3] * x_prime * y
    return x

def get_boundary_points(a, b, image):
    height = image.shape[0]
    boundary = np.zeros(height, 2)
    for y in range(height):
        boundary[y] = [a * y + b, y]
    return boundary

def straighten_margins(boundary_points, a):
    for row in boundary_points:
        forward_transform(row[0], row[1], a)
    return boundary_points[0][0]


def sort_text_lines(lines):
    lines = lines[np.argsort(lines[:, 0])]
    return lines

def find_top_bottom(line):
    return np.amax(line, axis=0)[1], np.amin(line, axis=0)[1]

def fit(lines, x_left, x_right):
    for line in lines:
        topY, bottomY = find_top_bottom(line)
        x = line[0]
        y = line[1]
        x = (x - x_left)/(x_right - x_left)
        y = (y - topY)/(bottomY - topY)









if __name__ == "__main__":
    array = np.array([[[0, 2], [4, 1], [2, 4]], [[9, 6], [1, 8], [5, 10]]])
    print("unsorted")
    print(array)
    print()
    print("sorted")
    print(sort_text_lines(array))






