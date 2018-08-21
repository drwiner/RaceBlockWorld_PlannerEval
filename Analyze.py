
PROBLEMS = [str(i) for i in range(27)]
SEARCH = "BestFirst".split()
SELECT = "E0 E3 E3Starx1 E3Starx2 E3Starx4 E3Starx6 E3Starx8 E3Starx16".split()
HEURISTIC = "AddReuseHeuristic ZeroHeuristic NumOCsHeuristic".split()

from collections import defaultdict

# 

#0 problem	12
#1 selection	E3Starx6-AddReuseHeuristic
#2 search	BestFirst
#3 runtime	36
#4 opened	43
#5 expanded	21
#6 primitives	12
#7 decomps	3
#8 composites	3
#9 hdepth	3

# 

PRIM_NAMES = "SinglePutdown SinglePickup SingleStroll".split()
COMP_NAMES = "MatchPutDown BlockGetaway duelShots TwoAgentTest".split()
RUNTIME_THRESHOLD = 600000

class PlanRun:
	
	
	def __init__(self, args):
		self.comp_dict=  defaultdict(int)
		self.has_comp = False
		
		self.problem = args[0]
		self.selection = args[1]
		self.search = args[2]
		self.heuristic = args[3]
		self.opened = args[4]
		self.expanded = args[5]
		self.runtime = args[6]
		if (self.runtime>= RUNTIME_THRESHOLD):
			self.solved = False
			self.primitives=  -1
			self.composites = -1
			self.hdepth = -1
		else:
			self.solved = True
			self.primitives = args[7]
			self.composites=  args[8]
			self.hdepth=  args[9]
		
	def addCompNames(self, comp_names):
		for cname in comp_names:
			self.comp_dict[cname] += 1
			if cname in COMP_NAMES:
				self.has_comp = True

	def __str__(self):
		return "{}-{}-{}-{}".format(self.problem, self.selection, self.search, self.heuristic);
				
			
def parseLine(line):
	sp = line.split()
	return sp[0], sp[1]

def IsBlank(line):
	if (line == "\n" or line == "" or line == None):
		return True
	return False
	
def organizePlanRunInput(pdict, selection, search, heuristic):
	organized_output = []
	organized_output.append(int(pdict["problem"]))
	organized_output.append(selection)
	organized_output.append(search)
	organized_output.append(heuristic)
	organized_output.append(int(pdict["opened"]))
	organized_output.append(int(pdict["expanded"]))
	organized_output.append(int(pdict["runtime"]))
	organized_output.append(int(pdict["primitives"]))
	organized_output.append(int(pdict["composites"]))
	organized_output.append(int(pdict["hdepth"]))
	return organized_output
	
def parseComposites(filename, starting_line):
	comp_names = []
	for i, line in enumerate(filename):
		if i < starting_line:
			continue
		if IsBlank(line):
			return comp_names
		
		sp = line.split()
		compName = sp[0][1:]
		comp_names.append(compName)
		
	return comp_names
	
def parseEverything(filename, selection, search, heuristic, prob):
	ending_line = 0

	paramDict= dict()
	for i, line in enumerate(filename):
		if (IsBlank(line)):
			ending_line = i+1
			break
		key, val = parseLine(line)
		paramDict[key] = val
	organized_args= organizePlanRunInput(paramDict, selection, search, heuristic)
	prun = PlanRun(organized_args)

	filename.seek(0)
	# fastforward to composites
	for i, line in enumerate(filename):
		if line == "Composites:\n" or line == "Composites":
			ending_line = i + 2
			break

	filename.seek(0)
	comp_names = parseComposites(filename, ending_line)
	prun.addCompNames(comp_names)
	return prun
	
		
		
			

if __name__ == "__main__":

	Solved = []
	UnSolved = []
	stringName = '{}-{}-{}-{}.txt'

	for selection in SELECT:
		for heuristic in HEURISTIC:
			for search in SEARCH:
				for prob in PROBLEMS:
					try:
						with open(stringName.format(prob, search, selection, heuristic), "r") as filename:
							print(stringName.format(prob, search, selection, heuristic))
							
							plan_run = parseEverything(filename, selection, search, heuristic, prob)
							if plan_run.solved:
								Solved.append(plan_run)
							else:
								UnSolved.append(plan_run)
					except:
						continue

	solvable_probs = set(pnum.problem for pnum in Solved)
	unsolvable_probs = set(pnum.problem for pnum in UnSolved if pnum.problem not in solvable_probs)

	print("solvable problems")
	for solvable in solvable_probs:
		print(solvable)
	print("\nUnsolvable problems:")
	for unsolved in unsolvable_probs:
		print(unsolved)

	has_comp_solution = []
	for prob in solvable_probs:
		solved_this_prob = [pnum for pnum in Solved if pnum.problem == prob and pnum.has_comp and pnum.solved]
		if (len(solved_this_prob) > 0):
			has_comp_solution.append(prob)


	print("check")
		
						
