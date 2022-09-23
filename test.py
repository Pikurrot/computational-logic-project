
temp = 0
option2 = ""
while option2 != "N":
	print("""MENU
1.- Addition
2.- Subtraction
3.- Multiplication
4.- Division
5.- Exit""")
	option = int(input("Select one option:"))
	option2 = "Y"
	while True:
		if 0<option<5:
			temp = option
			num1 = float(input())
			num2 = float(input())
			if option==1:
				print(f"{num1} + {num2} = {num1+num2}")
			elif option==2:
				print(f"{num1} - {num2} = {num1-num2}")
			elif option==3:
				print(f"{num1} * {num2} = {num1*num2}")
			elif option==4 and num2 != 0:
				print(f"{num1} / {num2} = {num1/num2}")
			else:
				print("Error: Division by Zero")
			break
		elif option == 5:
			option2 = input("Do you want to change the operands?")
			while option2 != "Y" and option2 != "N":
				option2 = input("Error. Do you want to change the operands?")
			if option2 == "N":
				print("Exiting the calculator ...")
				break
			else:
				option = temp
				continue
		else:
			print("Error: Invalid option")