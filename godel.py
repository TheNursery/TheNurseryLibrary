        #to each string the program assign a unique number given by a godel numeration. 
#The powers of the prime decomposition correspond to the keys in the dictionary alphabet. 
#Example: the word "godel" has associated the string (7,15,4,5,12) given by the keys in the dictionary; and godel number given by g=2^{7}3^{15}5^{4}7^{5]11^{12}.



import math
import sys
import numpy as np

import random
my_randoms = random.sample(xrange(100), 10)

alphabet={1 : "a",
2:"b",
3:"c",
4:"d",
5:"e",
6:"f",
7:"g",
8:"h",
9:"i",
10:"j",
11:"k",
12:"l",
13:"m",
14:"n",
15:"o",
16:"p",
17:"q",
18:"r",
19:"s",
20:"t",
21:"u",
22:"v",
23:"w",
24:"x",
25:"y",
26:"z"}     



noise = np.random.randint(0, 10000, size=10)




prime=[]
letters=[]
semigodel=[]
godel=[]
ruido=[]

#return the key of a given value in the dictionary
def key_for_value(alphabet, value):
  
    for k, v in alphabet.iteritems():
        if v == value:
            return k

 
my_randoms = random.sample(xrange(1000000), 10)

for i in range(10):
	if (my_randoms[i]%2!=0):
	        ruido.append(my_randoms[i])     

    
vnm= raw_input("Enter words: ")


words=vnm.split(" ")


for i in range (0,len(words)):
	var = words[i]
	if var=='':
	
			sys.exit(0)

  
	else: 
	
	                
			for num in range(2,1000):
  				if all(num%i!=0 for i in range(2,num)):
  					prime.append(num)     
				
			for i in range(0,len(var)):
       				if var[i] in alphabet.values():
         				letters.append(var[i]) 
      					
                        #godel numeration
			for i in range(0,len(var)):
        			semigodel.append(pow(prime[i],key_for_value(alphabet,letters[i])))
	                     	

		        g=reduce(lambda x, y: x * y, semigodel)
			       
                        godel.append(g)
                        
                        godel=godel+ruido
                       
                               
                        
                        del letters[:]
			del semigodel[:]

with open("test.txt", "a,r") as myfile:
     myfile.write(str(godel)+'\n')
			
                          

	
print godel
			
                        




