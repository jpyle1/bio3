from optparse import OptionParser
import random
import math

def getBetweenIndex(runTot,val):
	closestLessArr  = map(lambda x: val-x if val-x<0 else -1,runTot)
	closestLessMax = max(closestLessArr)
	closestLessIdx = closestLessArr.index(closestLessMax) 
	closestGreatArr = map(lambda x: val-x if val-x>0 else 1,runTot)
	closestGreatMin = min(closestGreatArr)
	closestGreatIdx = closestGreatArr.index(closestGreatMin)
	return (closestLessIdx,closestGreatIdx) 

def mutate(val,pm):
	p = random.random()
	if p < pm:
		if val == "0":
			return "1"
		else:
			return "0"	
	else:
		return val

def getFitness(x,l):
	return math.pow((x/math.pow(2,l)),10)
	
def run(l,N,G,pm,pc):
	#Actually do the computations.
	population = [random.getrandbits(l) for x in xrange(N)] 			
	#Display the population...		
	mapPop = lambda x,y :str(x)+":"+bin(y)[2:].zfill(l)+":"+str(y)
	#Initialize average fitness of the population array
	avgFit = [0 for x in xrange(G)]
	bestFit = [0 for x in xrange(G)]
	numCorr = [0 for x in xrange(G)]
	#popStr = "\n".join(map(mapPop,xrange(N),population))	
	#For Each generation, do the following:
	for gen in xrange(G):
		#For debug purposes..
		#popStr = "\n".join(map(mapPop,xrange(N),population))		
		#print "===\n"+popStr+"\n==="
		#Now, compute each fitness value.	
		fitnesses = [ getFitness(curr,l) for curr in population ]	
		#Get the best fit...
		bestFit[gen] = max(fitnesses)
		#Compute the overall sum of all the fitnesses	
		fitSum = sum(fitnesses)
		#Get the averageFit
		avgFit[gen] = fitSum/N
		#Keep an array of the normalized fitness values.
		fitNorm = map(lambda x: x/fitSum,fitnesses)	
		#Get the running total...
		runTot = [ sum(fitNorm[:x+1]) for x in xrange(N)]

		#Get the next generation
		nextGen = []
		#Perform N/2 iterations doing the following...
		for mate in xrange(N/2):
			parOne = 0
			parTwo = 0
			maxNumTries = 100	
			numTries = 0 
			#While the parents are equal
			while parOne == parTwo:
				if numTries > maxNumTries:
					break
				randOne = random.random()
				randTwo = random.random()	
				parOne = getBetweenIndex(runTot,randOne)[0]
				parTwo = getBetweenIndex(runTot,randTwo)[0]
				numTries+=1	
			#Determine if crossover will be done.
			cross = random.random()	
			#Copy the bits of the parents over...
			childOneBits  = bin(population[parOne])[2:].zfill(l)
			childTwoBits  = bin(population[parTwo])[2:].zfill(l)
			childOne = ""
			childTwo = ""

			if cross < pc:
				#Crossover is done.
				crossPoint = random.randint(0,l-1)
				childTwo+= childTwoBits[:crossPoint]
				childTwo+= childOneBits[crossPoint:]
				childOne+= childOneBits[:crossPoint]
				childOne+= childTwoBits[crossPoint:]
			else:
				childOne = childOneBits
				childTwo = childTwoBits	

			childOne = "".join([mutate(childOne[x],pm) for x in xrange(l)])
			childTwo = "".join([mutate(childTwo[x],pm) for x in xrange(l)])
			nextGen.append(int(childOne,2))
			nextGen.append(int(childTwo,2))

		population = nextGen
	print avgFit
	print "=="
	print bestFit
								
if __name__ == "__main__":
	#Set the default values.
	l = 20
	N = 30
	G = 10
	pm = .033
	pc = .66
	#Tell the parser what to parse.
	parser = OptionParser()
	parser.add_option("-N","--popSize")
	parser.add_option("-G","--generations")
	parser.add_option("-M","--mutation")
	parser.add_option("-C","--crossover")
	parser.add_option("-l","--numGenes")
	#Actually parse the arguments
	(options,args) = parser.parse_args()
	if(options.popSize is not None):
		N = int(options.popSize)
	if(options.generations is not None):
		G = int(options.generations)
	if(options.mutation is not None):
		pm = float(options.mutation)
	if(options.crossover is not None):
		pc = float(options.crossover)
	if(options.numGenes is not None):
		l = int(options.numGenes)
	#Display the selection to the user...		
	print "Selected Attributes"
	print "Number of Genes "+str(l)
	print "Population Size "+str(N)
	print "Number of Generations "+str(G)						
	print "Mutation Prob "+str(pm)
	print "CrossOver Prob "+str(pc)
	#Seed random.
	random.seed()
	run(l,N,G,pm,pc)
