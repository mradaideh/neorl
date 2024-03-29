from neorl import FNEAT
import numpy as np 

def Sphere(individual):
    """Sphere test objective function.
            F(x) = sum_{i=1}^d xi^2
            d=1,2,3,...
            Range: [-100,100]
            Minima: 0
    """
    return sum(x**2 for x in individual)

nx=5
lb=-100
ub=100
bounds={}
for i in range(1,nx+1):
        bounds['x'+str(i)]=['float', -100, 100]

# modify your own NEAT config
config = {
    'pop_size': 50,
    'num_hidden': 1,
    'activation_mutate_rate': 0.1,
    'survival_threshold': 0.3,
    }

fneat=FNEAT(fit=Sphere, bounds=bounds, mode='min', config= config, ncores=1, seed=1)
#some random guess (just one individual)
x0 = np.random.uniform(lb,ub,nx)
x_best, y_best, fneat_hist=fneat.evolute(ngen=5, x0=x0, verbose=True, 
                                          checkpoint_itv=None, startpoint=None) 

