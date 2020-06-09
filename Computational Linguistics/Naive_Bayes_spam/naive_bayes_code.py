import math

f = open('spam_assassin.train')
num_spam = 0.0
num_ham = 0.0
dict_spam = {}
dict_ham = {}
for line in f:
	# label, title = line.strip().split('\t')
	# words = title.split()
	blah = line.strip().split()
	label = blah[0] # spam if 1 ham if 0
	if label == '0': num_ham += 1
	elif label == '1': num_spam += 1
	words = blah[1:]#
	for word in words:
		if label == '0':
			if not word in dict_ham: dict_ham[word] = 0.0
			dict_ham[word] += 1
		elif label == '1':
			if not word in dict_spam: dict_spam[word] = 0.0
			dict_spam[word] += 1
f.close()

dict_ham['<UNK>'] = 0.0
dict_spam['<UNK>'] = 0.0
for word in dict_ham:
	dict_ham[word] += 1
for word in dict_spam:
	dict_spam[word] += 1
# 3. Convert the frequencies into probabilities.
p_ham = num_ham / (num_ham + num_spam) # P(C=ham)
p_spam = num_spam / (num_ham + num_spam) # P(C=spam)
total_spam = sum(dict_spam.values())
for word in dict_spam: dict_spam[word] /= total_spam # x /= y means x = x/y
total_ham = sum(dict_ham.values())
for word in dict_ham: dict_ham[word] /= total_ham # x /= y means x = x/y


# 4. Use the probabilities to classify each email in spam_assassin.test.



true_spam = 0.0 # hk
false_spam = 0.0 # hk
true_ham = 0.0 # hk
false_ham = 0.0 # hk
f = open('spam_assassin.test')
for line in f.readlines():
        blah = line.strip().split()
        label = blah[0]
        words = blah[1:]
        s_sum = math.log(p_spam)
        h_sum = math.log(p_ham)
	

        for word in words:
                if word in dict_spam:
                        s_sum += math.log(dict_spam[word])
                else:
                        s_sum += math.log(dict_spam['<UNK>'])
                if word in dict_ham:
                        h_sum += math.log(dict_ham[word])
                else:
                        h_sum += math.log(dict_ham['<UNK>'])
#

	if s_sum >= h_sum: # prediction = spam
        	if label == '1': # this is spam
                 	true_spam += 1
        	elif label == '0': #ham
                        false_spam += 1
    

	else: # prediction = ham 
			if label == '1':
					false_ham += 1 
			elif label == '0': 
					true_ham += 1 

# 5. Score the classification performance.

# 5.1. Precision = proportion of true spams out of all emails your program labeled spam
# 5.2. Recall = proportion of true spams out of all emails whose true label is spam






precision = true_spam / (true_spam + false_spam)
print 'Precision:', precision
recall = true_spam / (true_spam + false_ham)
print 'Recall:', recall















