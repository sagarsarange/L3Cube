'''
Write a code that verifies birthday paradox is indeed correct.
'''

import random, math
def birthday_gen():
        return int(math.ceil(random.uniform(0,365)))  		#generate random number from uniform dstribution of 365 numbers
def birthday_paradox(people):
        same = 0
        for x in range(0,10000):                      		#10000 sample tests
                i=[birthday_gen() for y in range(0,people)]  	#generate 'people' no. of random numbers
                if len(set(i))!=len(i): same = same+1  		#increment count if at least 2 numbers generated are same
        return str(round(same/float(x),3)*100)+"%" 	    	#calculate probability

print birthday_paradox(input("Number of people: "))  					#give input here
