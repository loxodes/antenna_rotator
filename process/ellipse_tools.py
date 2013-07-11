# functions for dealing fitting and computing information about ellipses
# from Nicky van Foreest's website, http://nicky.vanforeest.com/misc/fitEllipse/fitEllipse.html

def ellipse_plot(x, y):
    x = x[:-1]
    y = y[:-1]

    R = linspace(0, 2 * pi, len(x))
    a = fit_ellipse(x, y)
    center = ellipse_center(a)
    phi = ellipse_angle_of_rotation(a)
    a, b = ellipse_axis_length(a)
    xx = center[0] + a*np.cos(R)*np.cos(phi) - b*np.sin(R)*np.sin(phi)
    yy = center[1] + a*np.cos(R)*np.sin(phi) + b*np.sin(R)*np.cos(phi)

    scatter(x,y)
    plot(xx,yy, color = 'red')
    show()


# ellipse fitting technique from: http://nicky.vanforeest.com/misc/fitEllipse/fitEllipse.html
def fit_ellipse(x,y):
    x = x[:,np.newaxis]
    y = y[:,np.newaxis]
    D =  np.hstack((x*x, x*y, y*y, x, y, np.ones_like(x)))
    S = np.dot(D.T,D)
    C = np.zeros([6,6])
    C[0,2] = C[2,0] = 2; C[1,1] = -1
    E, V =  eig(np.dot(inv(S), C))
    n = np.argmax(np.abs(E))
    a = V[:,n]
    return a

# from: http://nicky.vanforeest.com/misc/fitEllipse/fitEllipse.html
def ellipse_center(a):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    num = b*b-a*c
    x0=(c*d-b*f)/num
    y0=(a*f-b*d)/num
    return np.array([x0,y0])

# from: http://nicky.vanforeest.com/misc/fitEllipse/fitEllipse.html
def ellipse_angle_of_rotation( a ):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    return 0.5*np.arctan(2*b/(a-c))

# ellipse axis length from: http://nicky.vanforeest.com/misc/fitEllipse/fitEllipse.html
def ellipse_axis_length( a ):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    up = 2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g)
    down1=(b*b-a*c)*( (c-a)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    down2=(b*b-a*c)*( (a-c)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    res1=np.sqrt(up/down1)
    res2=np.sqrt(up/down2)
    return np.array([res1, res2])

