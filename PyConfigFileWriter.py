import sys, os

# finds and returns the index for the end of a block in a string
# skips over nested blocks to match the correct one
def findEndOfBlock(startPos, inp, opener, closer):
	starts = [startPos]
	for i in range(len(inp)):
		if i <= startPos:
			continue
		if inp[i] == opener:
			starts.append(i)
		elif inp[i] == closer:
			if len(starts) > 1:
				starts.pop()
			else:
				return i
	return -1

# returns the position range of the (first) block identified by the preceding name
# example: name delimiter { block content }
def getNamedBlock(name, inp, offset = 0, nameDelim = "="):
	name = name + nameDelim
	p = inp.find(name)
	if p < -1:
		raise Exception("unknown name")

	p += len(name)
	block = inp[p:] # only search after the name position
	
	start = block.find("{")
	end = findEndOfBlock(start + p, inp, "{", "}")
	if start < 0 or end < 0:
		raise Exception("unknown block delimiter")
	# return positions relative to original input + offset
	return (start + p + 1 + offset, end + offset)
	
def getIndexBlock(i, inp, offset = 0, nameDelim = "="):
	return getNamedBlock("[" + str(i) + "]", inp, offset, nameDelim)

# returns the exact range of a named value (when defined on a single line)
# example: key delimiter value here \n
def getValRange(key, delim, inp, offset = 0):
	k = inp.find(key)
	d = inp[k:].find(delim)
	start = d + len(delim) + k
	end = inp[start:].find("\n") + start
	return (start + offset, end + offset)

# replaces a substring at specific position, returns modified copy
def strMod(pos, remNum, new, inp):
	a = inp[:pos]
	b = inp[pos+remNum:] 
	return a + new + b

def replaceSpecificValue(inp, blockName, subBlockIdx, valueName, newValue):
	# find the enclosing block
	r = getNamedBlock(blockName, inp, 0)
	block = inp[r[0]:r[1]]
	# find the indexed (nested) block
	r = getIndexBlock(subBlockIdx, block, r[0])
	block = inp[r[0]:r[1]]
	# find the value to change
	r = getValRange(valueName, "=", block, r[0])
	# change the value
	return strMod(r[0], r[1]-r[0], newValue, inp)

def main():
	print("Simon Liimatainen 2022")
	fileName = ""
	index = 0
	newValue = ""
	if len(sys.argv) != 4:
		print("Wrong number of arguments. Expected 3")
		print("Sorry, changing all indices at once is not yet implemented. Ask the author to do it.")
	else:
		fileName = sys.argv[1]
		index = int(sys.argv[2])
		newValue = sys.argv[3]

		if not os.path.isfile(fileName):
			print("File could not be found, expected absolute path")
			exit

		f = open(fileName, "r")
		inp = f.read()
		f.close()
		inp = replaceSpecificValue(inp, "SensorSettingsWithNames", index, "SocketIp", newValue)
		f = open(fileName, "w")
		f.write(inp)
		f.close()
		print("Done")


main()
