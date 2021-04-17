state = [[1,'no'], [2,'yes'], [2,'yes1'], [2,'yes2'], [2,'yes3'], [1,'no2'], [3,'err1'], [3,'err2'], [3,'err3'], [3,'err1'], [1,'no3'], [5,'None']]
onesf = []
twosf = []
thrsf = []

#code goes here
if state[0][0] == 1: onesf.append(state[0])
elif state[0][0] == 2: twosf.append(state[0])
else: thrsf.append(state[0])

for i in range(len(state)-1):
    if state[i][0] != state[i+1][0]:
        if state[i][0] == 1:
            onesf.append(state[i])
        elif state[i][0] == 2:
            twosf.append(state[i])
        elif state[i][0] == 3:
            thrsf.append(state[i])
        if state[i+1][0] == 1:
            onesf.append(state[i+1])
        elif state[i+1][0] == 2:
            twosf.append(state[i+1])
        elif state[i+1][0] == 3:
            thrsf.append(state[i+1])


print(onesf)
print(twosf)
print(thrsf)