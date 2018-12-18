#Tobisantoso
#https://github.com/tobisantoso
#github.com/tobisantoso

import getopt
import os, os.path
import sys
import struct
import numpy 

def main(argv):
	inputpath = ''
	outputpath = ''

	if(len(argv) < 1):
		exit(2)
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		exit(2)
	for opt, arg in opts:
		if opt == '-h' or arg[0] == '-':
			exit(0)
		elif opt in ("-i", "--ifile"):
			inputpath = arg
		elif opt in ("-o", "--ofile"):
			outputpath = arg
		else:
			exit(2)

	if(inputpath == '' or 
		outputpath == '' or
		not (os.path.isfile(inputpath))): exit(2)


	ifile = open(inputpath, "r")
	freqtable = []

	for i in range(256): 
		freqtable.append(0)

	while(1):
		iter = ifile.read(1)
		if(not iter): break

		index = ord(iter[0])
		freqtable[index] = freqtable[index] + 1;

	ifile.close()
	freqtuples = []

	for i in range(256):
		freqtuples.append([freqtable[i],i])	

	freqtuples.sort(key=lambda x: x[1]) 	
	dirtytree = (buildTree(freqtuples)) 
	tree = tuplesToBST(dirtytree)		

	codes = dict() 							
	assignCodes(tree, codes)			
											

	print("Perhitungan selesai")

	numpy.set_printoptions(formatter={'int':lambda x:hex(int(x))})
	for key, value in codes.items() :
		print ("0x" + format(key, "02X"), value)

	ofile = open(outputpath, "w")	
	ifile = open(inputpath, "r")

	while(1):
		iter = ifile.read(1)
		if(not iter):
			break
		ofile.write(encode(iter, codes))
		ofile.write(" ") 

	print("Ditulis untuk " + outputpath)
	print("Decoding dari " + outputpath + " to console.\n")
	ofile.close()

	
	ofile = open(outputpath, "r")
	input = ofile.read().split(" ")
	for s in input:
		sys.stdout.write(decode(s, tree)) 


def buildTree(tuples):
	while len(tuples) > 1 :
		leastTwo = tuple(tuples[0:2])                  
		theRest  = tuples[2:]                          
		combFreq = leastTwo[0][0] + leastTwo[1][0]     
		tuples   = theRest + [(combFreq,leastTwo)]     
		tuples.sort(key=lambda x: x[0])                             
	return tuples[0]           

def tuplesToBST (tree):
	p = tree[1] 
	if type(p) == type(int(0)) : return p 
	else : return (tuplesToBST(p[0]), tuplesToBST(p[1]))

def assignCodes (node, codes, pat=''):
	if type(node) == type(int(0)):
		codes[(node)] = pat
	else: 
		assignCodes(node[0], codes, pat + "0")  
		assignCodes(node[1], codes, pat + "1")   

def encode (s, codes) :
    output = ""
    for ch in s : 
    	output += codes[ord(ch)]
    return output

def decode (s, tree) :
    output = ""
    p = tree
    for bit in s :
        if bit == '0' : p = p[0]     
        else          : p = p[1]    
        if type(p) == type(int(0)) :
            output += chr(p)              
            p = tree                 
    return output

def exit(status):
	print('Try This: huffman.py -i <inputpath> -o <outputpath>')
	print('\nCompresses an input file using Huffman encoding.')
	sys.exit(status)

if __name__ == "__main__":
   main(sys.argv[1:])
