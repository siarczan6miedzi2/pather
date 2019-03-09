#import graphics as graph
import time as tm
import copy as cp
import random as rand
from timeit import default_timer as timer

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
	
def ssmall(lst):
	lsttemp = sorted(lst)
	return (lsttemp[2]) # second smallest distance is the third smallest element, because of 0 distance between the point and itself, which should not be considered

def main():

#	pt = [point( 1,  7), point(23, 17), point( 5,  6), point(13,  9),
#	      point( 6, 41), point(16, 37), point( 1,  8), point( 1,  0),
#		  point( 4, 21), point(11, 10), point( 3,  6), point( 7,  5),
#		  point(15, 22), point(20, 17)]

	pointsNo = rand.randint(10, 100)
	pt = []
	for i in range(pointsNo):
		pt.append(point(rand.random(), rand.random()))
	
	print("Preparing computation:")
	print("Path consists of %d points" % pointsNo)
	
	startTime = timer()
	
	# create graphics
	
#	frame = graph.GraphWin("pather", 1200, 800, autoflush = False)
#	frame.setCoords(-1, len(pt)+1, len(pt)+2, -1)
	
	dst = [] # table of distances (floats)
	
	for x in range(len(pt)):
		dsttemp = []
		for y in range(len(pt)):
			dsttemp.append(distance(pt[x], pt[y]))
		dst.append(dsttemp)
		
#	dstfield = [] # table of fields (rectangles)
#	
#	for x in range(len(pt)):
#		dstfieldtemp = []
#		for y in range(len(pt)):
#			dstfieldtemp.append(graph.Rectangle(graph.Point(x, y), graph.Point(x+1, y+1)))
#		dstfield.append(dstfieldtemp)
#		
#	for x in range(len(pt)):
#		for y in range(len(pt)):
#			dstfield[x][y].setFill("white") if x == y else dstfield[x][y].setFill("yellow")
#			dstfield[x][y].draw(frame)
			
#	dstlabel = [] # table of labels (texts represeting <dst> (floats))
#			
#	for x in range(len(pt)):
#		dstlabeltemp = []
#		for y in range(len(pt)):
#			dstlabeltemp.append(graph.Text(graph.Point(x+0.5, y+0.5), ""))
#		dstlabel.append(dstlabeltemp)
#		
#	for x in range(len(pt)):
#		for y in range(len(pt)):
#			dstlabel[x][y].setText("{0:.2f}".format(dst[x][y]))
#			dstlabel[x][y].setFace('courier')
#			dstlabel[x][y].setStyle('bold')
#			dstlabel[x][y].setSize(16)
#			dstlabel[x][y].draw(frame)
			
	dststate = [] # table of states (strings represented by fields colors)
			
	for x in range(len(pt)):
		dststatetemp = []
		for y in range(len(pt)):
			dststatetemp.append("na") if x == y else dststatetemp.append("wait")
		dststate.append(dststatetemp)
		
#	statestext = [] # list of state descriptions (side texts)
#	
#	for y in range(len(pt)):
#		statestext.append(graph.Text(graph.Point(len(pt)+1, y+0.5), ""))
#		
#	for x in range(len(pt)):
#		statestext[x].setFace('arial')
#		statestext[x].setStyle('bold')
#		statestext[x].setSize(16)
#		statestext[x].draw(frame)
			
#	frame.update()
	
	# ---------------------------------------------------------------------------
	
	maxx = 0
	tmplist = []
	
	for x in range(len(pt)):
		tmplist.append(ssmall(dst[x]))
		#print(tmplist)
		maxx = max(tmplist)
		
	#print (maxx)
		
	for x in range(len(pt)):
		for y in range(len(pt)):
			if (dst[x][y] > maxx):
				dststate[x][y] = "excl"
				
	# recreate graphics
	
#	for x in range(len(pt)):
#		for y in range(len(pt)):
#			# color the field
#			if (x == y): continue
#			if (dststate[x][y] == "wait"):
#				dstfield[x][y].setFill("yellow")
#			elif (dststate[x][y] == "conf"):
#				dstfield[x][y].setFill("green")
#			elif (dststate[x][y] == "excl"):
#				dstfield[x][y].setFill("red")
#			else: # programming error
#				print("The programmist f*cked up")
	
	dststateBackup = cp.deepcopy(dststate)
	
	step = 0
	
	failflag = False
	fineflag = True
	
	# quasi-macros
	
	WAIT = 0
	EXCL = 1
	CONF = 2
	
	probType = "trivial"
	
	while True:
	
		step += 1
#		print("step ", step, end = ": ")

		# check states
		
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
#			statestext[x].setText(str(waitno) + " / " + str(exclno) + " / " + str(confno))
#			frame.update()
			
		#if (step > 110):
		#	tm.sleep(2)
		#if (step == 78): break
		
		# finish if all marked
		
		endflag = True
		
		for x in range(len(pt)):
			if not (endflag): break
			for y in range(len(pt)):
				if not (endflag): break
				if (dststate[x][y] == "wait"): endflag = False
				
		if (endflag): break
		
		# detect fail
		
		if  not (failflag): # fail not (detected previously and being repaired)
			for x in range(len(pt)):
				if (states[x][WAIT] + states[x][CONF] < 2):
					failflag = True
					break
			
		if (failflag): # recreate state from last saved backup (before removing biggest)
#			print("fail detected")
			probType = "non-trivial"
			dststate = cp.deepcopy(dststateBackup)
			if (fineflag == False):
				probType = "fail"
				break
			fineflag = False
			
			# recreate graphics
			
			for x in range(len(pt)):
				waitno = 0
				exclno = 0
				confno = 0
				for y in range(len(pt)):
#					# color the field
#					if (x == y): continue
#					if (dststate[x][y] == "wait"):
#						dstfield[x][y].setFill("yellow")
#					elif (dststate[x][y] == "conf"):
#						dstfield[x][y].setFill("green")
#					elif (dststate[x][y] == "excl"):
#						dstfield[x][y].setFill("red")
#					else: # programming error
#						print("The programmist f*cked up")
					# modify the state summary
					if (dststate[x][y] == "wait"): waitno += 1
					elif (dststate[x][y] == "excl"): exclno += 1
					elif (dststate[x][y] == "conf"): confno += 1
				states.append((waitno, exclno, confno))
#				statestext[x].setText(str(waitno) + " / " + str(exclno) + " / " + str(confno))
#				frame.update()
			# no break - let the biggest one be accepted instead of being removed
		
		# exclude if 2 joints found
		
		twojointflag = False
		
		if  not (failflag): # fail not detected previously and being repaired
			for x in range(len(pt)):
				if (twojointflag): break
				if (states[x][WAIT] > 0 and states[x][CONF] == 2):
					for y in range(len(pt)):
						if (twojointflag): break
						if (dststate[x][y] == "wait"):
							dststate[x][y] = "excl"
							dststate[y][x] = "excl"
#							dstfield[x][y].setFill("red")
#							dstfield[y][x].setFill("red")
#							frame.update()
							twojointflag = True
						
		if (twojointflag):
#			print("two joints found")
			continue
		
		# fill found
		
		fillbreakflag = False
		
		if  not (failflag): # fail not detected previously and being repaired
			for x in range(len(pt)):
				if (fillbreakflag): break
				if (states[x][WAIT] > 0 and states[x][EXCL] == len(pt) - 3):
					for y in range(len(pt)):
						if (dststate[x][y] == "wait"):
							dststate[x][y] = "conf"
							dststate[y][x] = "conf"
#							dstfield[x][y].setFill("green")
#							dstfield[y][x].setFill("green")
#							frame.update()
							fillbreakflag = True
						
		if (fillbreakflag):
#			print("row filled")
			continue
		
		# find biggest
	
		maxdist = 0
	
		for x in range(len(pt)):
			for y in range(len(pt)):
				if (dststate[x][y] == "wait" and dst[x][y] > maxdist): maxdist = dst[x][y]
		
		if  (failflag): # fail detected previously - to be repaired: accept biggest
			exclflag = False
	
			for x in range(len(pt)):
				if (exclflag): break
				for y in range(len(pt)):
					if (exclflag): break
					if (dst[x][y] == maxdist and dststate[x][y] == "wait"):
#						dstfield[x][y].setFill("green")
#						dstfield[y][x].setFill("green")
						dststate[x][y] = "conf"
						dststate[y][x] = "conf"
#						frame.update()
						exclflag = True
			failflag = False
#			print("biggest number accepted")
	
		else: # remove biggest
			dststateBackup = cp.deepcopy(dststate)
			fineflag = True
			exclflag = False
	
			for x in range(len(pt)):
				if (exclflag): break
				for y in range(len(pt)):
					if (exclflag): break
					if (dst[x][y] == maxdist and dststate[x][y] == "wait"):
#						dstfield[x][y].setFill("red")
#						dstfield[y][x].setFill("red")
						dststate[x][y] = "excl"
						dststate[y][x] = "excl"
#						frame.update()
						exclflag = True
					
#			print("biggest number removed")
	
#	if not (fineflag): print("Failed in step ", step)
#	print("Done")
#	print()

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
	
#	frame.getMouse()
#	frame.close()
	
if __name__ == "__main__": main()
