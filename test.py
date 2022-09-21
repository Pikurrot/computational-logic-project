
time = input("Enter the time with format hh:mm:ss = ")

hh = int(time[0:2])
mm = int(time[3:5])
ss = int(time[6:8])

ss+=1
if (ss >= 60):
	ss = 0
	mm += 1
if (mm >= 60):
	mm = 0
	hh += 1
if (hh >= 24):
	ss = 0
	mm = 0
	hh = 0

hh = "0"*(hh<10)+str(hh)
mm = "0"*(mm<10)+str(mm)
ss = "0"*(ss<10)+str(ss)

print(f"{hh}:{mm}:{ss}")