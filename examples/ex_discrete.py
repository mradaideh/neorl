from neorl import DE, GWO, SSA, WOA, AEO, MFO, JAYA, HHO, BAT, CS, EDEV, EPSO, PESA, PESA2, HCLPSO, PSO
from neorl import ES, SA
import math, random

#################################
# Define Vessel Function 
#Mixed discrete/continuous/grid
#################################
def Vessel(individual):
    """
    Pressure vesssel design
    x1: thickness (d1)  --> discrete value multiple of 0.0625 in 
    x2: thickness of the heads (d2) ---> categorical value from a pre-defined grid
    x3: inner radius (r)  ---> cont. value between [10, 200]
    x4: length (L)  ---> cont. value between [10, 200]
    """
    
    x=individual.copy()
    x[0] *= 0.0625   #convert d1 to "in" 

    y = 0.6224*x[0]*x[2]*x[3]+1.7781*x[1]*x[2]**2+3.1661*x[0]**2*x[3]+19.84*x[0]**2*x[2];

    g1 = -x[0]+0.0193*x[2];
    g2 = -x[1]+0.00954*x[2];
    g3 = -math.pi*x[2]**2*x[3]-(4/3)*math.pi*x[2]**3 + 1296000;
    g4 = x[3]-240;
    g=[g1,g2,g3,g4]
    
    phi=sum(max(item,0) for item in g)
    eps=1e-5 #tolerance to escape the constraint region
    penality=1e7 #large penality to add if constraints are violated
    
    if phi > eps:  
        fitness=phi+penality
    else:
        fitness=y
    return fitness

def init_sample(bounds):
    #generate an individual from a bounds dictionary
    indv=[]
    for key in bounds:
        if bounds[key][0] == 'int':
            indv.append(random.randint(bounds[key][1], bounds[key][2]))
        elif bounds[key][0] == 'float':
            indv.append(random.uniform(bounds[key][1], bounds[key][2]))
        elif bounds[key][0] == 'grid':
            indv.append(random.sample(bounds[key][1],1)[0])
        else:
            raise Exception ('unknown data type is given, either int, float, or grid are allowed for parameter bounds')   
    return indv
    
ngen=5

for item in ['mixed', 'grid', 'float/int', 'float/grid', 'int/grid', 'float', 'int']:
    bounds = {}
    btype=item  #float, int, grid, float/int, float/grid, int/grid, mixed. 
    
    print(item, 'is running -----')
    if btype=='mixed':
        bounds['x1'] = ['int', 1, 99]
        bounds['x2'] = ['grid', (0.0625, 0.125, 0.1875, 0.25, 0.3125, 0.375, 0.4375, 0.5, 0.5625, 0.625)]
        bounds['x3'] = ['float', 10, 200]
        bounds['x4'] = ['float', 10, 200]
        bounds['x5'] = ['grid', ('Hi', 'Bye', 'New')]
        bounds['x6'] = ['int', -5, 5]
    
    elif btype=='int/grid':      
        bounds['x1'] = ['int', 1, 20]
        bounds['x2'] = ['grid', (0.0625, 0.125, 0.1875, 0.25, 0.3125, 0.375, 0.4375, 0.5, 0.5625, 0.625)]
        bounds['x3'] = ['int', 10, 200]
        bounds['x4'] = ['int', 10, 200]
        bounds['x5'] = ['grid', ('Hi', 'Bye', 'New')]
        bounds['x6'] = ['int', -5, 5]
    
    elif btype=='float/grid':      
        bounds['x1'] = ['float', 1, 20]
        bounds['x2'] = ['grid', (0.0625, 0.125, 0.1875, 0.25, 0.3125, 0.375, 0.4375, 0.5, 0.5625, 0.625)]
        bounds['x3'] = ['float', 10, 200]
        bounds['x4'] = ['float', 10, 200]
        bounds['x5'] = ['grid', ('Hi', 'Bye', 'New')]
        bounds['x6'] = ['float', -5, 5]
        
    elif btype=='float/int':      
        bounds['x1'] = ['int', 1, 20]
        bounds['x2'] = ['float', 1, 20]
        bounds['x3'] = ['int', 10, 200]
        bounds['x4'] = ['float', 10, 200]
        bounds['x5'] = ['float', -5, 5]
        bounds['x6'] = ['int', -5, 5]
    
    elif btype=='float':      
        bounds['x1'] = ['float', 1, 20]
        bounds['x2'] = ['float', 1, 20]
        bounds['x3'] = ['float', 10, 200]
        bounds['x4'] = ['float', 10, 200]
        bounds['x5'] = ['float', -5, 5]
        bounds['x6'] = ['float', -5, 5]
        
    elif btype=='int':      
        bounds['x1'] = ['int', 1, 20]
        bounds['x2'] = ['int', 1, 20]
        bounds['x3'] = ['int', 10, 200]
        bounds['x4'] = ['int', 10, 200]
        bounds['x5'] = ['int', -5, 5]
        bounds['x6'] = ['int', -5, 5]
        
    elif btype=='grid':      
        bounds['x1'] = ['grid', (0.0625, 0.125, 0.375, 0.4375, 0.5625, 0.625)]
        bounds['x2'] = ['grid', (0.0625, 0.125, 0.1875, 0.25, 0.3125, 0.375, 0.4375, 0.5, 0.5625, 0.625)]
        bounds['x3'] = ['grid', (1,2,3,4,5)]
        bounds['x4'] = ['grid', (32,64,128)]
        bounds['x5'] = ['grid', ('Hi', 'Bye', 'New')]
        bounds['x6'] = ['grid', ('Cat', 'Dog', 'Bird', 'Fish')]
        
    ########################
    # Setup and evolute GWO
    ########################
    npop=70
    x0=[]
    for i in range(npop):
        x0.append(init_sample(bounds))
        
    gwo=GWO(mode='min', fit=Vessel, bounds=bounds, nwolves=npop, ncores=1, seed=1)
    x_gwo, y_gwo, gwo_hist=gwo.evolute(ngen=ngen, x0=x0, verbose=0)
    assert Vessel(x_gwo) == y_gwo

    ########################
    # Setup and evolute WOA
    ########################
    woa=WOA(mode='min', bounds=bounds, fit=Vessel, nwhales=npop, a0=1.5, b=1, ncores=1, seed=1)
    x_woa, y_woa, woa_hist=woa.evolute(ngen=ngen, x0=x0, verbose=0)
    #print(woa_hist['last_pop'])
    assert Vessel(x_woa) == y_woa

    ########################
    # Setup and evolute SSA
    ########################
    #setup and evolute SSA
    ssa=SSA(mode='min', bounds=bounds, fit=Vessel, nsalps=npop, int_transform='sigmoid', ncores=1, seed=1)
    x_ssa, y_ssa, ssa_hist=ssa.evolute(ngen=ngen, x0=x0, verbose=0)
    assert Vessel(x_ssa) == y_ssa
    
    ########################
    # Setup and evolute DE
    ########################
    de=DE(mode='min', bounds=bounds, fit=Vessel, npop=npop, F=0.5, CR=0.7, int_transform='sigmoid', ncores=1, seed=1)
    x_de, y_de, de_hist=de.evolute(ngen=ngen, x0=x0, verbose=0)
    #print(de_hist['last_pop'])
    assert Vessel(x_de) == y_de
    
    ########################
    # Setup and evolute MFO
    ########################
    mfo=MFO(mode='min', bounds=bounds, fit=Vessel, nmoths=npop, int_transform='minmax', ncores=1, seed=1)
    x_mfo, y_mfo, mfo_hist=mfo.evolute(ngen=ngen, x0=x0, verbose=0)
    #print(mfo_hist['last_pop'])
    assert Vessel(x_mfo) == y_mfo

    ########################
    # Setup and evolute JAYA
    ########################
    jaya=JAYA(mode='min', bounds=bounds, fit=Vessel, npop=npop, int_transform='sigmoid', ncores=1, seed=1)
    x_jaya, y_jaya, jaya_hist=jaya.evolute(ngen=ngen, x0=x0, verbose=0)
    #print(jaya_hist['last_pop'])
    assert Vessel(x_jaya) == y_jaya
    
    ########################
    # Setup and evolute HHO
    ########################
    hho = HHO(mode='min', bounds=bounds, fit=Vessel, nhawks=npop, 
                      int_transform='minmax', ncores=1, seed=1)
    x_hho, y_hho, hho_hist=hho.evolute(ngen=ngen, x0=x0, verbose=0)
    #print(hho_hist['last_pop'])
    assert Vessel(x_hho) == y_hho

    ########################
    # Setup and evolute BAT
    ########################
    bat=BAT(mode='min', bounds=bounds, fit=Vessel, nbats=npop, fmin = 0 , fmax = 1, 
            A=0.5, r0=0.5, levy = True, seed = 1, ncores=1)
    x_bat, y_bat, bat_hist=bat.evolute(ngen=ngen, x0=x0, verbose=0)
    #print(bat_hist['last_pop'])
    assert Vessel(x_bat) == y_bat

    ########################
    # Setup and evolute CS
    ########################
    #cs = CS(mode = 'min', bounds = bounds, fit = Vessel, ncuckoos = npop, pa = 0.25, seed=1)
    #x_cs, y_cs, cs_hist=cs.evolute(ngen=ngen, x0=x0, verbose=0)
    #print(cs_hist['last_pop'])
    #assert Vessel(x_cs) == y_cs
    
    ########################
    # Setup and evolute EDEV
    ########################
    edev=EDEV(mode='min', bounds=bounds, fit=Vessel, npop=npop, ncores=1, seed=1)
    x_edev, y_edev, edev_hist=edev.evolute(ngen=100, x0=x0, ng=10, verbose=0)
    #print(edev_hist['last_pop'])
    assert Vessel(x_edev) == y_edev

    ########################
    # Setup and evolute EPSO
    ########################
    epso=EPSO(mode='min', bounds=bounds, g1=int(npop/2), g2=int(npop/2), fit=Vessel, ncores=1, seed=1)
    x_epso, y_epso, epso_hist=epso.evolute(ngen=100, x0=x0, LP=3, verbose=0)
    #print(epso_hist['last_pop'])
    assert Vessel(x_epso) == y_epso

    ########################
    # Setup and evolute HCLPSO
    ########################
    hclpso=HCLPSO(mode='min', bounds=bounds, g1=int(npop/2), g2=int(npop/2), fit=Vessel, ncores=1, seed=1)
    x_hclpso, y_hclpso, pso_hist=hclpso.evolute(ngen=100, x0=x0, verbose=0)
    #print(pso_hist['last_pop'])
    assert Vessel(x_hclpso) == y_hclpso
    
    ########################
    # Setup and evolute PSO
    ########################
    pso=PSO(mode='min', bounds=bounds, fit=Vessel, c1=2.05, c2=2.1, npar=npop,
                    speed_mech='constric', ncores=1, seed=1)
    x_pso, y_pso, pso_hist=pso.evolute(ngen=ngen, x0=x0, verbose=0)
    #print(pso_hist['last_pop'])
    assert Vessel(x_pso) == y_pso
    
    ########################
    # Setup and evolute ES 
    ########################
    es = ES(mode='min', fit=Vessel, cxmode='cx2point', bounds=bounds, 
                     lambda_=npop, mu=30, cxpb=0.7, mutpb=0.2, seed=1)
    x_es, y_es, es_hist=es.evolute(ngen=ngen, x0=x0, verbose=0)
    print(es_hist['last_pop'])
    assert Vessel(x_es) == y_es

    ########################
    # Setup and evolute SA 
    ########################
    
    #define a custom moving function
    def my_move(x, **kwargs):
        #-----
        #this function selects two random indices in x and perturb their values
        #-----
        x_new=x.copy()
        indices=random.sample(range(0,len(x)), 2)
        for i in indices:
            x_new[i] = random.uniform(bounds['x1'][1],bounds['x1'][2])
        
        return x_new
    
    #setup and evolute a serial SA
    sa=SA(mode='min', bounds=bounds, fit=Vessel, chain_size=npop, chi=0.2, Tmax=10000,
          move_func=my_move, reinforce_best='soft', cooling='boltzmann', ncores=1, seed=1)

    #setup and evolute parallel SA with `equilibrium` cooling
    #sa=SA(mode='min', bounds=BOUNDS, fit=FIT, chain_size=20, chi=0.2, Tmax=10000, threshold = 1, lmbda=0.05,
    #      move_func=my_move, reinforce_best='soft', cooling='equilibrium', ncores=8, seed=1)
    
    #x_best, y_best, sa_hist=sa.evolute(ngen=100, x0=x0[0], verbose=1)
    
    ########################
    # Setup and evolute PESA
    ########################
#    pesa=PESA(mode='min', bounds=bounds, fit=Vessel, npop=npop, mu=30, alpha_init=0.01,
#              alpha_end=1.0, cxpb=0.7, mutpb=0.2, alpha_backdoor=0.05)
#    x_pesa, y_pesa, pesa_hist=pesa.evolute(ngen=ngen, x0=x0, verbose=0)
#    #print(pesa_hist['last_pop'])
#    assert Vessel(x_pesa) == y_pesa

    ########################
    # Setup and evolute PESA2
    ########################
#    pesa2=PESA2(mode='min', bounds=bounds, fit=Vessel, npop=npop, nwolves=5)
#    x_pesa2, y_pesa2, pesa2_hist=pesa2.evolute(ngen=ngen, x0=x0, replay_every=2, verbose=0)
#    #print(pesa2_hist['last_pop'])
#    assert Vessel(x_pesa2) == y_pesa2
    

    ########################
    # Setup and evolute AEO
    ########################
    aeo = AEO(mode='min', bounds=bounds, optimizers=[de, gwo, woa, jaya, hho, pso, es, ssa], gen_per_cycle=3, fit = Vessel)
    x_aeo, y_aeo, aeo_hist = aeo.evolute(30, verbose = 0)
    assert Vessel(x_aeo) == y_aeo
        
    if 0:
        
        print('---Best GWO Results---')
        print(x_gwo)
        print(y_gwo)
        print('---Best WOA Results---')
        print(x_woa)
        print(y_woa)
        print('---Best SSA Results---')
        print(x_ssa)
        print(y_ssa)
        print('---Best DE Results---')
        print(x_de)
        print(y_de)
        print('---Best AEO Results---')
        print(x_aeo)
        print(y_aeo)