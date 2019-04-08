import time as tm # for sleep() (won't be needed finally)
import copy as cp
import random as rand # for terting random maps (won't be needed finally)
from timeit import default_timer as timer # for timing (will remain useful, not necessary though)

class point:
	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)
		
	def __str__(self):
		return (str(self.x) + ',' + str(self.y))
		
	__repr__ = __str__
		
	def getX(self): return self.x
	
	def getY(self): return self.y
	
def distance(p1, p2):
	return (((p1.getX()-p2.getX())**2+(p1.getY()-p2.getY())**2)**(1/2))
	
def ssmall(lst, n):
	lsttemp = sorted(lst)
	return (lsttemp[n])
	# n-th smallest distance is the (n+1)-th smallest element,
	# because of 0 distance between the point and itself,
	# which should not be considered

def main():

# --------------------------- CREATE TABLE OF POINTS --------------------------- #

	# this set fails before the improvement
	#pt = [point(15,  7), point(13, 27), point(15, 26), point(23,  9),
	 #     point(17, 21), point(12, 37), point(17, 18), point(11, 37)]
		  #point( 4, 21), point(11, 17), point( 3, 16), point( 7,  5),
		  #point(15, 22), point(20, 17), point( 0,  0)]

	#pointsNo = len(pt)
#	pointsNo = 8
		  
	#pointsNo = rand.randint(10, 100)
	pointsNo = 30
	pt = []
	for i in range(pointsNo):
		pt.append(point(rand.random(), rand.random()))

# ----------------------------- START THE ALGORITHM ----------------------------- #
	
	print("Preparing computation:")
	print("Path consists of %d points" % pointsNo)
	
	startTime = timer()
	
# ------------------- CREATE TABLE OF DISTANCES AND GRAPHICS ------------------- #
	
	
	dst = [] # table of distances (floats)
	
	for x in range(len(pt)):
		dsttemp = []
		for y in range(len(pt)):
			dsttemp.append(distance(pt[x], pt[y]))
		dst.append(dsttemp)
			
	dststate = [] # table of states (strings represented by fields colors)
			
	for x in range(len(pt)):
		dststatetemp = []
		for y in range(len(pt)):
			dststatetemp.append("na") if x == y else dststatetemp.append("wait")
		dststate.append(dststatetemp)

	probType = "trivial"

	for macroit in range(2, pointsNo-2):
	
	# ---------------------------- RESTORE BLANK TABLE ---------------------------- #

		for x in range(len(pt)):
			for y in range(len(pt)):
				dststate[x][y] = "na" if x == y else "wait"
	
		if (macroit > 2):
			probType = str(macroit)
	
	# ---------------------- REMOVE OBVIOUS UNUSED DISTANCES ---------------------- #
		
		maxx = 0
		tmplist = []
		
		for x in range(len(pt)):
			tmplist.append(ssmall(dst[x], macroit))
			maxx = max(tmplist)
			
		for x in range(len(pt)):
			for y in range(len(pt)):
				if (dst[x][y] > maxx):
					dststate[x][y] = "excl"

	# --------------------------- STORE THE CURRENT STATE --------------------------- #

		dststateBackup = [] # here all encountered states will be stored
					
		dststateBackup.append(cp.deepcopy(dststate))
		
		step = 0
		
		failflag = False
		fineflag = True
		deadflag = False
		
		# quasi-macros
		
		WAIT = 0
		EXCL = 1
		CONF = 2

	# ----------------- PROCEED WITH THE MAIN PART OF THE ALGORITHM ----------------- #
		
		while True:
		
			step += 1

	# ---------------------------- CHECK CURRENT STATES ---------------------------- #
			
			states = []
			
			for x in range(len(pt)):
				waitno = 0
				exclno = 0
				confno = 0
				for y in range(len(pt)):
					if (dststate[x][y] == "wait"): waitno += 1
					elif (dststate[x][y] == "excl"): exclno += 1
					elif (dststate[x][y] == "conf"): confno += 1
				states.append((waitno, exclno, confno))

	# ------------------- EVERY POINT HAS TWO DISTANCES: SUCCESS ------------------- #
			
			endflag = True
			
			for x in range(len(pt)):
				if not (endflag): break
				for y in range(len(pt)):
					if not (endflag): break
					if (dststate[x][y] == "wait"): endflag = False
					
			if (endflag): break # success: exit the program
			
	# ------------------------------- DETECT FAILURE ------------------------------- #
			
			if  not (failflag): # no fail has beed detected
				for x in range(len(pt)):
					if (states[x][WAIT] + states[x][CONF] < 2):
						failflag = True
						break
				
			if (failflag) and not (deadflag): # fail detected, but no so-previously-called dead-end
				if (macroit == 2): probType = "non-trivial"
				if (len(dststateBackup) == 0): # nothing possible to be restored
					if (macroit == 2): probType = "failed" # consider as fail
					break # fail: exit this iteration: try with less strict begin
				dststate = cp.deepcopy(dststateBackup.pop()) # restore the saved state
				if (fineflag == False): # so-previously-called dead-end reached
					dststate = cp.deepcopy(dststateBackup.pop()) # restore the earlier state
					deadflag = True
					continue
				fineflag = False

				# don't end this loop iteration; let the biggest distance be accepted instead of being removed
			
	# ----- TWO DISTANCES CONFIRMED FOR ONE POINT: REMOVE ALL WAITING (IF LEFT) ----- #
			
			twojointflag = False
			
			if  not (failflag): # no fail has been detected
				for x in range(len(pt)):
					if (twojointflag): break
					if (states[x][WAIT] > 0 and states[x][CONF] == 2):
						for y in range(len(pt)):
							if (twojointflag): break
							if (dststate[x][y] == "wait"):
								dststate[x][y] = "excl"
								dststate[y][x] = "excl"
								twojointflag = True
							
			if (twojointflag):
				continue
			
	# -------------- TWO POSSIBLE DISTANCES FOR A POINT: CONFIRM THEM -------------- #
			
			fillbreakflag = False
			
			if  not (failflag): # no fail has been detected
				for x in range(len(pt)):
					if (fillbreakflag): break
					if (states[x][WAIT] > 0 and states[x][EXCL] == len(pt) - 3):
						for y in range(len(pt)):
							if (dststate[x][y] == "wait"):
								dststate[x][y] = "conf"
								dststate[y][x] = "conf"
								fillbreakflag = True
							
			if (fillbreakflag):
				continue
			
	# ------------------------- FIND THE BIGGEST DISTANCE ------------------------- #
		
			maxdist = 0
		
			for x in range(len(pt)):
				for y in range(len(pt)):
					if (dststate[x][y] == "wait" and dst[x][y] > maxdist): maxdist = dst[x][y]
			
			if  (failflag): # fail has been detected - to be repaired: accept the biggest distance
			# do if even if deadflag
				exclflag = False
		
				for x in range(len(pt)):
					if (exclflag): break
					for y in range(len(pt)):
						if (exclflag): break
						if (dst[x][y] == maxdist and dststate[x][y] == "wait"):
							dststate[x][y] = "conf"
							dststate[y][x] = "conf"
							exclflag = True
				failflag = False
		
			else: # no fail - normal work - remove the biggest distance
				dststateBackup.append(cp.deepcopy(dststate)) # save current state before proceeding
				fineflag = True
				exclflag = False
		
				for x in range(len(pt)):
					if (exclflag): break
					for y in range(len(pt)):
						if (exclflag): break
						if (dst[x][y] == maxdist and dststate[x][y] == "wait"):
							dststate[x][y] = "excl"
							dststate[y][x] = "excl"
							exclflag = True
						
		if (endflag): break
		
	print("Done")
	print()

	endTime = timer()

	print("Problem type:", probType)
	print("Time elapsed: %.3f seconds" % (endTime - startTime))
	print()
	res = open("types", 'a+')
	res.write(str(pointsNo))
	res.write('\t')
	res.write(probType)
	res.write('\t')
	res.write(str(endTime-startTime))
	res.write('\n')
	res.close()
	
if __name__ == "__main__": main()
