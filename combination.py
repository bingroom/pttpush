import numpy as np

def getCombination(n):
	c = (n*n -n)/2
	A = np.zeros([c,2],dtype = np.uint16)
	
	addingArray = np.array(range(1,n), dtype=np.uint16)
	start = 0
	end = 0


	for element in range(n-1):
		start = end
		end = start + n-1 - element
		A[:,0][start:end] = element
		
	print("Array A finished")
	
	end = 0
	
	for element in range(n-1):
		start = end
		end = start + n-1 - element

		elementListLen = n-1 - element
		
		
		
		
		A[:,1][start:end] = addingArray[element:]
		
	print("Array B finished")
	return A

