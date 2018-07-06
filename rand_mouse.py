import numpy as np
import scipy.interpolate as si
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

def movement ():
	points = [[0, 0], [4, 7], [3, 4], [8, 0]] #curve base
	points = np.array(points)

	x = points[:,0]
	y = points[:,1]

	t = range(len(points))
	ipl_t = np.linspace(0.0, len(points) - 1, 10)

	x_tup = si.splrep(t, x, k=3)
	y_tup = si.splrep(t, y, k=3)

	x_list = list(x_tup)
	xl = x.tolist()
	x_list[1] = xl + [0.0, 0.0, 0.0, 0.0]

	y_list = list(y_tup)
	yl = y.tolist()
	y_list[1] = yl + [0.0, 0.0, 0.0, 0.0]

	x_i = si.splev(ipl_t, x_list) #x interolate values
	y_i = si.splev(ipl_t, y_list) #y_interpolate values

	return x_i, y_i


