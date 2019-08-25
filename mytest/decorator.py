import time 
import math 

def deco_calc_time(function):
	def inner(*args, **kwargs): 
		begin = time.time() 
		function(*args, **kwargs) 
		end = time.time() 
		print("Execution time of", function.__name__, ":",end - begin) 
	return inner
 
@deco_calc_time
def factorial(num):  
	time.sleep(2) 
	print(math.factorial(num)) 

factorial(10)
