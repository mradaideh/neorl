#--------------------------------------------------------------------
# Paper: NEORL: A Framework for NeuroEvolution Optimization with RL
# Section: Script for section 4.3
# Contact: Majdi I. Radaideh (radaideh@mit.edu)
# Last update: 9/10/2021
#---------------------------------------------------------------------

#Setup Google Drive
import os
from neorl import HHO, ES, PESA, BAT, GWO

#Basic packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import cv2 #for plotting the MIT reactor core
import time

#Sklearn tools
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import MinMaxScaler

#Keras specials
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import Adam
from keras.layers.normalization import BatchNormalization
from keras.regularizers import L1L2

#External path
mitr_path='mitr_temp.png'
noisy_data=True
#----------------------------------------------------------------
#                           Load data
#----------------------------------------------------------------

#---------------------------
#(a). Load data from url
xurl='./data/crx.csv'
if noisy_data:
    yurl='./data/final_noisy_powery.csv'
else:
    yurl='./data/powery.csv'
xdata=pd.read_csv(xurl)
ydata=pd.read_csv(yurl)
colnames=list(ydata.columns)

#---------------------------
#(b). Understand the data structure
print(xdata.head()) # view the first 5 rows of the dataset
print(ydata.head()) # view the first 5 rows of the dataset
print(xdata.shape)
print(ydata.shape)

xdata=xdata.values # convert dataframe to numpy array
ydata=ydata.values # convert dataframe to numpy array

gen_noisy_data=False

if gen_noisy_data:
    noise_level=np.random.uniform(1,2)/100    #1%-2% is typical noise in reactor power
    for i in range(0,300):                    #add noise to first 300 samples
        for j in range(ydata.shape[1]):
            noise_value=np.random.normal(0, noise_level*ydata[i,j]) 
            ydata[i,j] = ydata[i,j] + noise_value
    
    ydf=pd.DataFrame(ydata, columns=colnames)
    ydf.to_csv('noisy_powery.csv', index=False)
    

#---------------------------
#(c). Data split for training/testing
xtrain=xdata[0:800,:]  #use clean and noisy data in training
ytrain=ydata[0:800,:]  #use clean and noisy data in training

xtest=xdata[800:,:]   #use only clean data for testing
ytest=ydata[800:,:]   #use only clean data for testing

#---------------------------
#(d). Input/output scaling
# Create min-max scaling object
xscaler = MinMaxScaler()
yscaler = MinMaxScaler()

# Apply scaling on the input data
Xtrain=xscaler.fit_transform(xtrain)
Xtest=xscaler.transform(xtest)

# Apply scaling on the output data
Ytrain=yscaler.fit_transform(ytrain)
Ytest=ytest.copy()


#----------------------------------------------------------------
#                         Model Builder
#----------------------------------------------------------------
def fitness(inp):
     
    num_layers=int(inp[0]) 
    learning_rate=inp[1]
    batch_size=int(inp[2])
    dropout=inp[3]
    num_nodes=inp[4:]
    epochs=10
    # Create the deep learning model.
    model = Sequential()
    model.add(Dense(int(num_nodes[0]), kernel_initializer='normal', activation='relu', input_dim=Xtrain.shape[1]))
    model.add(Dropout(rate=dropout))
    for i in range(1, num_layers):
      model.add(Dense(int(num_nodes[i]), activation='relu', kernel_initializer='normal'))
    model.add(Dense(Ytrain.shape[1], activation='linear', kernel_initializer='normal'))
            
    model.compile(loss='mean_absolute_error', optimizer=Adam(learning_rate), metrics=['mean_absolute_error'])
    #model.summary()
    
    # train the model
    model.fit(Xtrain, Ytrain, epochs=epochs, batch_size=batch_size, 
              validation_split = 0.15, verbose=False, shuffle=True)

    # Get the R2 score on the test-set
    Ynn=model.predict(Xtest)
    # apply inverse transform to get real power values
    Ynn=yscaler.inverse_transform(Ynn)
    
    mae=mean_absolute_error(Ytest,Ynn)
    mse=mean_squared_error(Ytest,Ynn)
    R2=r2_score(Ytest,Ynn)
    
    #print the results
    print('parameters=', inp, 'MAE=', np.round(mae,3))
    
    return mae


#----------------------------------------------------------------
#                         NEORL Optimization
#----------------------------------------------------------------
bounds = {}
bounds['num_layers'] = ['int', 2, 7]
bounds['learning_rate'] = ['float', 1e-4, 1e-3]
bounds['batch_size'] = ['grid', (8, 16, 32, 64, 128)]
bounds['dropout'] = ['float', 0.0, 0.5]
bounds['n_nodes1'] = ['int', 100, 200]
bounds['n_nodes2'] = ['int', 100, 150]
bounds['n_nodes3'] = ['int', 100, 150]
bounds['n_nodes4'] = ['int', 50, 100]
bounds['n_nodes5'] = ['int', 50, 100]
bounds['n_nodes6'] = ['int', 25, 50]
bounds['n_nodes7'] = ['int', 25, 50]

npop=10
ngen=10
ncores=10
colnames=list(bounds.keys()) + ['MAE']
algs=['PESA', 'HHO', 'ES', 'BAT', 'GWO']
results=np.zeros((len(algs), len(colnames)))
if 1:
    
    
    ########################
    # Setup and evolute PESA
    ########################
    t0=time.time()
    pesa=PESA(mode='min', bounds=bounds, fit=fitness, npop=npop, mu=5, 
              alpha_init=0.01, cxpb=0.7, mutpb=0.2, ncores=ncores*3, seed=1)
    x_pesa, y_pesa, pesa_hist=pesa.evolute(ngen=ngen, warmup=11, verbose=1)
    print('PESA time=', time.time()-t0)
    results[0, :-1]=x_pesa
    results[0, -1]=y_pesa
    
    ########################
    # Setup and evolute HHO
    ########################
    t0=time.time()
    hho = HHO(mode='min', bounds=bounds, fit=fitness, nhawks=npop,
                      int_transform='minmax', ncores=ncores, seed=1)
    x_hho, y_hho, hho_hist=hho.evolute(ngen=ngen, verbose=1)
    print('HHO time=', time.time()-t0)
    results[1, :-1]=x_hho
    results[1, -1]=y_hho
    
    ########################
    # Setup and evolute ES
    ########################
    t0=time.time()
    es = ES(mode='min', fit=fitness, cxmode='cx2point', bounds=bounds,
                     lambda_=npop, mu=5, cxpb=0.7, mutpb=0.2, ncores=ncores, seed=1)
    x_es, y_es, es_hist=es.evolute(ngen=ngen, verbose=1)
    print('ES time=', time.time()-t0)
    results[2, :-1]=x_es
    results[2, -1]=y_es
    
    ########################
    # Setup and evolute BAT
    ########################
    t0=time.time()
    bat=BAT(mode='min', bounds=bounds, fit=fitness, nbats=npop, fmin = 0 , fmax = 1,
            A=0.5, r0=0.5, levy = True, ncores=ncores, seed=1)
    x_bat, y_bat, bat_hist=bat.evolute(ngen=ngen, verbose=1)
    print('BAT time=', time.time()-t0)
    results[3, :-1]=x_bat
    results[3, -1]=y_bat
    
    ########################
    # Setup and evolute GWO
    ########################
    t0=time.time()
    gwo=GWO(mode='min', fit=fitness, bounds=bounds, nwolves=npop, ncores=ncores, seed=1)
    x_gwo, y_gwo, gwo_hist=gwo.evolute(ngen=ngen, verbose=1)
    print('GWO time=', time.time()-t0)
    results[4, :-1]=x_gwo
    results[4, -1]=y_gwo
    
    

########################
# Comparison
########################
print('---Best HHO Results---')
print(x_hho)
print(y_hho)
print('---Best ES Results---')
print(x_es)
print(y_es)
print('---Best PESA Results---')
print(x_pesa)
print(y_pesa)
print('---Best BAT Results---')
print(x_bat)
print(y_bat)
print('---Best GWO Results---')
print(x_gwo)
print(y_gwo)

results=pd.DataFrame(results, index=algs, columns=colnames)
sort_results = results.sort_values(['MAE'], axis='index', ascending=True)
print(sort_results)
sort_results.to_csv('control_tune.csv', index=True)

best_inp=list(sort_results.iloc[0,:].values[0:-1])  #exclude R2
print(best_inp)
#----------------------------------------------------------------
#                Rerun with the best hyperparameters
#----------------------------------------------------------------

num_layers=int(best_inp[0]) 
learning_rate=best_inp[1]
batch_size=int(best_inp[2])
dropout=best_inp[3]
num_nodes=best_inp[4:]
epochs=10
# Create the deep learning model.
model = Sequential()
model.add(Dense(int(num_nodes[0]), kernel_initializer='normal', activation='relu', input_dim=Xtrain.shape[1]))
model.add(Dropout(rate=dropout))
for i in range(1, num_layers):
  model.add(Dense(int(num_nodes[i]), activation='relu', kernel_initializer='normal'))
model.add(Dense(Ytrain.shape[1], activation='linear', kernel_initializer='normal'))
        
model.compile(loss='mean_absolute_error', optimizer=Adam(learning_rate), metrics=['mean_absolute_error'])
model.summary()

# train the model
history=model.fit(Xtrain, Ytrain, epochs=epochs, batch_size=batch_size, validation_split = 0.15, verbose=False)

# obtain the training/validation MAE from fitting history
train_err=history.history['mean_absolute_error']
val_err=history.history['val_mean_absolute_error']

# plot the training/validation MAE on the same plot
plt.figure()
plt.plot(train_err, label='Training')
plt.plot(val_err, label='Validation')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()

Ynn=model.predict(Xtest)
# apply inverse transform to get real power values
Ynn=yscaler.inverse_transform(Ynn)

mae=mean_absolute_error(Ytest,Ynn)
rmse=np.sqrt(mean_squared_error(Ytest,Ynn))
r2=r2_score(Ytest,Ynn)
print('MAE=',mae, 'RMSE=',rmse, 'R2=', r2)

#-------------------------------------------------------
#                MITR Pattern Plot
#-------------------------------------------------------
# Plotter function for MITR
def plot_mitr (model, x, yscaler=None):
    pos=[(400,330), (465,230), (500,300), (395,400), (320,400), (285,255), (318,193),
         (500,165), (535,230), (575,295), (535,360), (500, 430), (430, 465), (355, 465), (280, 465),
         (240,400), (205, 335), (210,255), (243,193), (280,130), (355,130), (430,130),
         (393,193), (460,360), (280, 335), (400,265), (340,295)]
    
    Ynn=model.predict(np.array([x,]))
    if yscaler:
        Ynn=yscaler.inverse_transform(Ynn)
    Ynn=Ynn.flatten().tolist()
    
    image = cv2.imread(mitr_path)
    for i in range(len(pos)):
        if i==0:
            image=cv2.putText(img=np.copy(image), text=str(int(Ynn[i])), org=pos[i], fontFace=1, fontScale=1.1, color=(0,0,0))
        if i in [1,2,3,4,5,6]:
            image=cv2.putText(img=np.copy(image), text=str(int(Ynn[i])), org=pos[i], fontFace=1, fontScale=1.1, color=(0,0,255)) 
        if i in list(range(7,22)):
            image=cv2.putText(img=np.copy(image), text=str(int(Ynn[i])), org=pos[i], fontFace=1, fontScale=1.1, color=(0, 100, 0)) 
        if i in list(range(22,28)):
            image=cv2.putText(img=np.copy(image), text=str('Empty'), org=pos[i], fontFace=1, fontScale=1.1, color=(233, 150, 122))            
    cv2.imwrite("mitr_res.jpg", image, [int(cv2.IMWRITE_JPEG_QUALITY), 300])
    plt.imshow(image)
    plt.show()

#---------------------------
#(f). Show the reactor plot of MITR
print('---(f)---')
x=[0.75266553, 0.90280633, 0.00539489, 0.25308624, 0.57678792, 0.77792903]
plot_mitr(x=x, model=model, yscaler=yscaler)
# To show the reator plot in high quality in Google Colab
#from IPython.display import Image
#Image('mitr.jpg')
