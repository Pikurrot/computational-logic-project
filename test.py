def fibonacci(n):
	a = 0
	b = 1
	if n == 0:
		return 0
	while n > 1:
		sum = a+b
		a = b
		b = sum
		n -= 1
	return b

n = int(input("Enter n: "))
while n < 0:
	print("Error: Number cannot be negative")
	n = int(input("Enter n: "))
f = fibonacci(n)
print(f"The {n} term of the Fibonacci series is {f}")