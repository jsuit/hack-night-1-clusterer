__author__ = 'jsuit'
from corpus import Corpus
import numpy as np
from numpy import matlib
import time
import pprint
import sklearn

t0 = time.time()
k=50
alpha = .01
beta = .001
sampleFile = 'ap.txt'
#sampleFile = 'ap2.text'
sample_vocab = 'vocab.txt'
corpus = Corpus()


corpus.num_docs = corpus.getNumOfSampleDocs(sampleFile)
corpus.vocab,corpus.num_terms = corpus.getSampleVocab(sample_vocab)
corpus.readDocsSample(sampleFile)
#document-topic
DTMatrix = matlib.zeros((corpus.num_docs,k),dtype='float_')
#term,topic matrix
TTMatrix =matlib.zeros((corpus.num_terms,k),dtype='float_')
vocab_index_dict = {word.rstrip():index for index, word in enumerate(corpus.vocab)}
vocab_word_dict = {index:word for word,index in vocab_index_dict.iteritems()}
DocVocab = {}
#doc is an int

for doc_num,words in corpus.docs.iteritems():
        #sample topic index for word
        #each word in a document gets assigned a topic
        #words = set(vocab_index_dict.keys()) & set(words)
        #print 'On doc %d' % doc_num
        for word in words:

                pz = np.divide(np.multiply(DTMatrix[doc_num,:] + alpha,
                        (TTMatrix[vocab_index_dict[word],:] + beta)),DTMatrix.sum(axis=0) + beta*corpus.num_terms)

                sample_pz= np.random.multinomial(1, np.asarray(pz/pz.sum())[0],1)
                topic = sample_pz.argmax()
                #if we've seen the word in the document before and it's been assigned
                #to a different topic
                if (doc_num,word) not in  DocVocab:
                        DocVocab[(doc_num,word)] = topic
                else:
                        topic = DocVocab[(doc_num,word)]
                DTMatrix[doc_num,topic] +=1
                TTMatrix[vocab_index_dict[word],topic]+=1


        #increase counters in matrices
        #increase count in Document topic matrix
for i in xrange(100):
        print i
        for doc_num,words in corpus.docs.iteritems():
                #words = set(vocab_index_dict.keys()) & set(words)
                for word in words:
                        topic = DocVocab[(doc_num,word)]
                        TTMatrix[vocab_index_dict[word],topic]-=1
                        DTMatrix[doc_num,topic]-=1

                        #sample
                        #(n(d,k) + alpha_k)(n_k,w+B_w/n_k)

                        pz = np.divide(np.multiply(DTMatrix[doc_num,:] + alpha,
                        (TTMatrix[vocab_index_dict[word],:] + beta)),DTMatrix.sum(axis=0) + beta*corpus.num_terms)
                        sample_pz  = np.random.multinomial(1, np.asarray(pz/pz.sum())[0],1)
                        topic = sample_pz.argmax()

                        DocVocab[(doc_num,word)] = topic
                        TTMatrix[vocab_index_dict[word],topic]+=1
                        DTMatrix[doc_num,topic]+=1

kDist = {}

for index in xrange(corpus.num_terms):
        #for each word look at the number of times it has been assigned to k
        #TTMatrix[index,:]
        #topicDistribution for word_i

        #topic = t_dist_w_i.argmax()
        #m = np.max(t_dist_w_i)
        t_dist_w_i = np.divide(TTMatrix[index,:]+beta, TTMatrix.sum(axis=0)+beta*corpus.num_terms)
        t_dist_w_i = np.asarray(t_dist_w_i)[0]
        for k_c in xrange(k):
                if not kDist or k_c not in kDist:
                        kDist[k_c] = [(vocab_word_dict[index],t_dist_w_i[k_c])]
                elif len(kDist[k_c]) <= 7:
                        m_list = kDist[k_c]
                        m_list.append((vocab_word_dict[index],t_dist_w_i[k_c]))
                        kDist[k_c] =  sorted(m_list,key = lambda t: t[1])

                else:
                        mlist = kDist[k_c]
                        minscore = min(mlist, key = lambda t: t[1])
                        #print minscore,t_dist_w_i[k_c]
                        if t_dist_w_i[k_c]>minscore[1]:
                                for (word,score) in mlist:
                                        if score == minscore[1]:
                                                mlist.remove((word,score))
                                                mlist.append((vocab_word_dict[index],t_dist_w_i[k_c]))
                                                kDist[k_c] =  sorted(mlist,key = lambda t: t[1])
                                                break

t1 = time.time()
print t1-t0
with open('topic.txt','w') as f:
                for key in vocab_index_dict.iterkeys():
                        f.write(key.rjust(4)+', ')
                        t_dist_w_i = np.divide(TTMatrix[vocab_index_dict[key],:]+beta, TTMatrix.sum(axis=0)+beta*corpus.num_terms)
                        t_dist_w_i = np.asarray(t_dist_w_i)[0]
                        for i in xrange(TTMatrix.shape[1]):
                                f.write('    '+str(t_dist_w_i[i])+ ',    ')
                        f.write('\n')
f.close()



print pprint.pprint(kDist)






