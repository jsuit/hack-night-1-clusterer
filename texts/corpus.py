import Document
import loadData
import numpy as np
class Corpus():

        def __init__(self):
                self.docs = {}
                self.num_docs = 0
                self.num_terms = 0
                self.vocab = None
        def getNumOfSampleDocs(self,sampleFile):
                return loadData.getNumOfDocs(sampleFile)

        def getVocabSize(self,sampleFile):
                return loadData.getVocabSizeSample('ap.txt')

        def getSampleVocab(self, sampleFile ='vocab.txt'):
                self.vocab,self.num_terms = loadData.getSampleVocab(self, sampleFile ='vocab.txt')

                return self.vocab,self.num_terms

        def readDocsSample(self, sampleFile):
                for i, (key,text) in enumerate(loadData.docGeneratorSample(sampleFile)):
                        self.docs[i] =  list(set(self.vocab) & set(text))

