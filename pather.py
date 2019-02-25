import graphics as graph
import time as tm

class point:
	def __init__(self, x, y):
		self.x = float(x)
		self.y = float(y)
		
	def str(self):
		return (self.x + ',' + self.y)
		
	def getX(self): return self.x
	
	def getY(self): return self.y
	
def distance(p1, p2):
	return (((p1.getX()-p2.getX())**2+(p1.getY()-p2.getY())**2)**(1/2))

def main():
	pt = [point(3,  0), point( 3, 2), point( 5,  4), point( 5, 9),
	      point(7,  2), point( 5, 7), point(10,  0), point( 5, 0),
		  point(3, 10), point(10, 6), point( 9,  4), point(10, 5),
		  point(11, 3)]
		
	#print(dst)
	
	frame = graph.GraphWin("pather", 1200, 800, autoflush = False)
	frame.setCoords(-1, len(pt)+1, len(pt)+2, -1)
	
	dst = []
	
	for x in range(len(pt)):
		dsttemp = []
		for y in range(len(pt)):
			dsttemp.append(distance(pt[x], pt[y]))
		dst.append(dsttemp)
		
	dstfield = []
	
	for x in range(len(pt)):
		dstfieldtemp = []
		for y in range(len(pt)):
			dstfieldtemp.append(graph.Rectangle(graph.Point(x, y), graph.Point(x+1, y+1)))
		dstfield.append(dstfieldtemp)
		
	for x in range(len(pt)):
		for y in range(len(pt)):
			dstfield[x][y].setFill("white") if x == y else dstfield[x][y].setFill("yellow")
			dstfield[x][y].draw(frame)
			
	dstlabel = []
			
	for x in range(len(pt)):
		dstlabeltemp = []
		for y in range(len(pt)):
			dstlabeltemp.append(graph.Text(graph.Point(x+0.5, y+0.5), ""))
		dstlabel.append(dstlabeltemp)
		
	for x in range(len(pt)):
		for y in range(len(pt)):
			dstlabel[x][y].setText("{0:.2f}".format(dst[x][y]))
			dstlabel[x][y].setFace('courier')
			dstlabel[x][y].setStyle('bold')
			dstlabel[x][y].setSize(16)
			dstlabel[x][y].draw(frame)
			
	dststate = []
			
	for x in range(len(pt)):
		dststatetemp = []
		for y in range(len(pt)):
			dststatetemp.append("na") if x == y else dststatetemp.append("wait")
		dststate.append(dststatetemp)
		
	statestext = []
	
	for y in range(len(pt)):
		statestext.append(graph.Text(graph.Point(len(pt)+1, y+0.5), ""))
		
	for x in range(len(pt)):
		statestext[x].setFace('arial')
		statestext[x].setStyle('bold')
		statestext[x].setSize(16)
		statestext[x].draw(frame)
			
	frame.update()
	
	# ---------------------------------------------------------------------------
	
	step = 0
	
	failflag = False
	
	# quasi-macros
	
	WAIT = 0
	EXCL = 1
	CONF = 2
	
	while True:
	
		step += 1
		print("step ", step, end = ": ")

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
			statestext[x].setText(str(waitno) + " / " + str(exclno) + " / " + str(confno))
			frame.update()
			
		#if (step == 64): break
			
		#tm.sleep(0.5)
		
		# finish if all marked
		
		endflag = True
		
		for x in range(len(pt)):
			if not (endflag): break
			for y in range(len(pt)):
				if not (endflag): break
				if (dststate[x][y] == "wait"): endflag = False
				
		if (endflag): break
		
		# detect fail
		
		for x in range(len(pt)):
			if (states[x][WAIT] + states[x][CONF] < 2):
				failflag = True
				break
			
		if (failflag):
			print("fail detected")
			break
		
		# exclude if 2 joints found
		
		twojointflag = False
		
		for x in range(len(pt)):
			if (twojointflag): break
			if (states[x][WAIT] > 0 and states[x][CONF] == 2):
				for y in range(len(pt)):
					if (twojointflag): break
					if (dststate[x][y] == "wait"):
						dststate[x][y] = "excl"
						dststate[y][x] = "excl"
						dstfield[x][y].setFill("red")
						dstfield[y][x].setFill("red")
						frame.update()
						twojointflag = True
						
		if (twojointflag):
			print("two joints found")
			continue
		
		# fill found
		
		fillbreakflag = False
		
		for x in range(len(pt)):
			if (fillbreakflag): break
			if (states[x][WAIT] > 0 and states[x][EXCL] == len(pt) - 3):
				for y in range(len(pt)):
					if (dststate[x][y] == "wait"):
						dststate[x][y] = "conf"
						dststate[y][x] = "conf"
						dstfield[x][y].setFill("green")
						dstfield[y][x].setFill("green")
						frame.update()
						fillbreakflag = True
						
		if (fillbreakflag):
			print("row filled")
			continue
		
		# find biggest
	
		maxdist = 0
	
		for x in range(len(pt)):
			for y in range(len(pt)):
				if (dststate[x][y] == "wait" and dst[x][y] > maxdist): maxdist = dst[x][y]
		
		# remove biggest
	
		exclflag = False
	
		for x in range(len(pt)):
			if (exclflag): break
			for y in range(len(pt)):
				if (exclflag): break
				if (dst[x][y] == maxdist and dststate[x][y] == "wait"):
					dstfield[x][y].setFill("red")
					dstfield[y][x].setFill("red")
					dststate[x][y] = "excl"
					dststate[y][x] = "excl"
					frame.update()
					exclflag = True
					
		print("biggest number removed")
	
	if (failflag): print("Fail detected in step ", step)
	else: print("Done")
	
	frame.getMouse()
	frame.close()
	
if __name__ == "__main__": main()
