import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import math

df = pd.read_csv("data/raw/lichess-08-2014.csv")

#print(df.head())
#print(df.info())

df = df.sort_values('Rating Difference', ascending = True)

word_to_num = {'White Wins': 50, 'Black Wins': -50, 'Draw': 0}
num_array = [word_to_num.get(word,word) for word in df['Result']]

bin_length = 10

data = np.column_stack([df['Rating Difference'], num_array])

# print (data)


empty_list = []
xList = []

index = 0

split = 1000

max = len(data)

total = 0   
splitIndex = 0
start = data[index][0]

while(index < max):

    if(splitIndex < split):
        total += data[index][1]
        splitIndex+=1
        index+=1
        
    else:
        empty_list.append(total/splitIndex)
        xList.append((start + data[index][0])/2)
        splitIndex=0
        total = 0
        start = data[index][0]
        
empty_list.append(total/splitIndex)
xList.append((start + data[max-1][0])/2)
    
# print(empty_list)
# print(xList)

newData = np.vstack([xList, empty_list])
# print(newData)

degree = 3
coefficients = np.polyfit(newData[0], newData[1], deg=3)

# Create polynomial function
poly_function = np.poly1d(coefficients)

x_smooth = np.linspace(-1000,1000,200)
y_pred = poly_function(x_smooth)

st.title("Rating Difference vs Match Outcome")
st.write("Visualizing the trend between rating difference and match result")

fig, ax = plt.subplots()

plt.scatter(xList, empty_list, s = 1)
plt.plot(x_smooth, y_pred, color = 'red')
plt.title('Rating Difference Vs Outcome')
plt.xlabel('Rating dif')
plt.ylabel('Result')
plt.show()

st.pyplot(fig)