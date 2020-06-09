# 1. Load the pickle files into dictionaries:
# import pickle
# A = pickle.load(open('A.pickle'))
# likewise for B

#importing files#
# 2.3. run the Viterbi algorithm on the list



#Task statement: We want to build a bigram part-of-speech (POS) tagger. I have all the necessary probabilities: transition
#probabilities P(t2|t1) and emission probabilities P(w|t). You implement the Viterbi algorithm to finish
#building the tagger in Python and see how good the tagger is.


import sys, pickle, math

def build_trellis(word_list, A, B):
	trellis = [ {'<s>':[0.0, None]} ]#crumb that we assign to the beginning of string=none
	for w in word_list[1:]:
		# 1. Identify possible tags, which become the keys in our dictionary.
		# 1.1. the possible tag should first be reachable from a state in the previous column.
		reachables = []
		prev_states = trellis[-1].keys()

		for ps in prev_states: reachables += A[ps].keys() #A=transition prob. dictionary, adding the possible reachable tags to the reachables
		reachables = set(reachables)#set is a collection, likely an EQUALSUNIQUE, eliminating duplicates
		# 1.2. further filter reachables by only keeping states that can generate the word w
		column = {}
		for state in reachables:
			if w in B[state]: #looking in emissions prob, seeing what word we could get to, and the sate we're considering should be able to emit the word to make sure it makes sense  
				column[state] = [-1e+100, None]
		# 2. Update the deltas and the crumbs.
		#for state in reachables: # Sorry, we just further filtered reachables...
		for state in column: # makes more sense to use column instead
			for ps in prev_states: #working one column at a time
				try:
					score = trellis[-1][ps][0] # delta of ps
					score += math.log(A[ps][state]) # log transition prob
					score += math.log(B[state][w]) # log emission pro b score includes all three, current best store, transition prob, and emission
					if score > column[state][0]: # best score so far?
						column[state][0] = score
						column[state][1] = ps
				except KeyError: pass
		# 3. Append the column to our trellis.
		trellis.append(column)
	return trellis

#now must backtrace, test
#how?
def traceback(trellis):
	crumbs=[]#we'll start w. end of sentence b/c it's obvious crumb
	crumbs.append('</s>')
	reverse_trellis=trellis[::-1]
	for column in reverse_trellis:
		try:
			c=column[crumbs[-1]][1] #doing col is starting out at s column, the column is a dict. w. keys, keys are tags, we looking for tag that matching last added crumb, a particular column might have multiple tags	
			crumbs.append(c)
		except KeyError: pass
	crumbs.reverse()
		
	return crumbs[2:-1]

			
				


#From class, I think what I already did
if __name__ == '__main__':
        A = pickle.load(open('A.pickle'))
        B = pickle.load(open('B.pickle'))
        f = open('brown.test')
        #i = 1
        for line in f:
                word_list = ['<s>']+line.strip().split()+['</s>']
		#print word_list #UNCOMMENT LATER
        t = build_trellis(word_list, A, B)
		#print t #UNCOMMENT LATER
        crumbs=traceback(t)
	crumbs=crumbs[2:-1]
                #print crumbs #UNCOMMENT LATER
  #              word_list=word_list[1:-1]
 #              	tagged_sentence = " "
#                for j in range(len(crumbs)):
                        #rest will be emailed
      
               #i += 1
	f.close()

#remaining to do eemove first 2 prefixes, last suffixes from the traceback 

##calcing accuracy


#(2) You should compare crumbs with the tags in the answer file. Recall that the answer file has each word tagged in word_#_tag format. So for each line in the answer file,
#(2-1) Create two lists: a list of words and a list of tags. For example, if the line were 'this_DT is_VBZ good_JJ' then you should convert that to ['this', 'is', 'good'] and ['DT', 'VBZ', 'JJ'].
	right=0.0
	wrong=0.0
	yours=open('brown.test.answers').readlines()
	
	for line in yours:
		#tried to tag lines w. end of sentence, but that failedsplit=['<s>']+line.strip().split()+['</s>']
		split_line=line.strip().split()
#		for i in range(len(split_line)):
#			if split_line[i]==".":
#				split_line.insert(i,'</s>')
		your_word_list=[] #I thought words should be listed outside loop, but will try
		your_tags=[]	
		for pairs in split_line:
			word,tag=pairs.split('_#_')
			#your_word_list.append('<s>')
			#your_word_list.append('</s>')
			your_word_list.append(word)
			your_tags.append(tag)

# hk: fixed indentations below
		print "these are tags"		
		print your_tags
		print "length"
		print len(your_tags)
		print "this is the word list"
		print your_word_list

		#(2-2) Run the viterbi algorithm (i.e. build_trellis and traceback) on the word list to get the crumb, i.e. the predicted sequence of tags.
		#(2-3) Compare the crumb from 2-2 with the tag list from 2-1
			#def accuracy(trellis, yours):
			#i+=1	
		#running build_trellis and traceback on answer words
		print "this is the trellis"

		answer=build_trellis(['<s>']+your_word_list+['</s>'], A, B) # hk: you need to pad wordlist with <s> and </s>
#		print answer
#		print 'traceback results'
		answer_crumbs=traceback(answer)
#		print answer_crumbs#prob is prob. here ##Is there the end of sentence tag? I get a keyerror
		#answer_crumbs=answer_crumbs[2:-1] # hk: I see that you already sliced crumbs to crumbs[2:-1] in your traceback function so no need to slice again.
#		print "these are crumbs"
#		print answer_crumbs
		print len(answer_crumbs)
		for i in range(len(your_tags)): #enumerate makes it so we can do rows columns, could try that 
			#for index, crumb in enumerate(crumbs):
			if your_tags[i]==answer_crumbs[i]:
				right+=1
			else: 
				wrong+=1
		
		accuracy=right/(right+wrong)
		print "precision"
		print accuracy

