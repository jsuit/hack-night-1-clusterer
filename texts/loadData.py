__author__ = 'jsuit'

import os
from collections import defaultdict

def loadData(file):
        pass

def getNumOfDocs(samplefile):
        #/Users/jsuit/PycharmProjects/hack-night-1-clusterer/ap.txt
        project_root_directory = os.path.join(os.path.dirname(__file__), '../')
        data_file = os.path.join(project_root_directory, samplefile)
        print 'The data file path is {0}'.format(data_file)
        counter = 0
        with open(data_file) as f:
                for line in f:
                        mline = line.split()
                        if len(mline) != 0:
                                if mline[0] == '<DOCNO>':
                                        counter +=1
        f.close()
        return counter

def getVocabSizeSample(samplefile):

        project_root_directory = os.path.join(os.path.dirname(__file__), '../')
        data_file = os.path.join(project_root_directory, samplefile)
        print 'The data file path is {0}'.format(data_file)
        with open(data_file) as f:
                lines = [line.rstrip() for line in f]
        f.close()
        return len(lines)

def getVocab(samplefile):
        project_root_directory = os.path.join(os.path.dirname(__file__), '../')
        data_file = os.path.join(project_root_directory, samplefile)
        print 'The data file path is {0}'.format(data_file)
        with open(data_file) as f:
                lines = f.readlines()
        f.close()
        return lines

def docGeneratorSample(sampleFile):
        project_root_directory = os.path.join(os.path.dirname(__file__), '../')
        data_file = os.path.join(project_root_directory, sampleFile)
        with open(data_file,'r') as f:
                key = None
                inside_doc = False
                for line in f:
                        line_split = line.split()
                        if len(line_split):
                                if line_split[0].rstrip() == '<DOCNO>':
                                        key = line_split[1]
                                        inside_doc = True
                                elif inside_doc == True:
                                        if line_split[0].rstrip()!= '<TEXT>':
                                                inside_doc = False
                                                yield key, line_split


def getSampleVocab(self, sampleFile ='vocab.txt'):
        project_root_directory = os.path.join(os.path.dirname(__file__), '../')
        data_file = os.path.join(project_root_directory, sampleFile)
        with open(data_file) as f:
                lines = [line.rstrip().lower() for line in f]

        f.close()
        return lines,len(lines)