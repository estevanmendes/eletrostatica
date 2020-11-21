from laplace_cartesian_v1 import *
dim=10
rounds=10
capacitor=poisson_equation(dim,dim,realism=True)
cem=np.ones(dim)*100
cem_2=np.ones(dim+2)*100

zero=np.zeros(dim)
capacitor.contour_rectangle_capacitor(cem,-cem,zero,zero)
resultado=capacitor.run(rounds=100)
capacitor.plot2d()
capacitor.plot3d()