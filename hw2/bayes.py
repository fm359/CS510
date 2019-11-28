import sys, math, os, pickle, re, string

class Bayes_Classifier:

   def __init__(self, trainDirectory = "movies_reviews/movies_reviews/"):
      '''This method initializes and trains the Naive Bayes Sentiment Classifier.  If a 
      cache of a trained classifier has been stored, it loads this cache.  Otherwise, 
      the system will proceed through training.  After running this method, the classifier 
      is ready to classify input text.'''
      self.trainDir = trainDirectory     # store training directory as an attribute

      # Check if pickle files exist. If so, load dictionaries of +ve and -ve words
      # If not, initialize them and train the classifier.
      if os.path.exists("negative_reviews.p") and os.path.exists("positive_reviews.p"):
         self.negativeReviews = self.load("negative_reviews.p")
         self.positiveReviews = self.load("positive_reviews.p")
         self.numNegativeDocs = len(self.negativeReviews) # total number of -ve documents
         self.numPositiveDocs = len(self.positiveReviews) # total number of +ve documents
         self.sumNegativeFeatures = sum(self.negativeReviews.values()) # total number of -ve words
         self.sumPositiveFeatures = sum(self.positiveReviews.values()) # total number of +ve words
      else:
         self.negativeReviews = {}
         self.positiveReviews = {}
         self.numNegativeDocs = 0
         self.numPositiveDocs = 0
         self.sumNegativeFeatures = 0
         self.sumPositiveFeatures = 0
         self.train()

   def train(self):   
      '''Trains the Naive Bayes Sentiment Classifier.'''
      iFileList = []
      for fFileObj in os.walk(self.trainDir):
         iFileList = fFileObj[2]
         break

      # Obtain review score from text file name, create a list of all words in the file
      # for each word, add it to the appropriate dictionary and save to pickle files.
      for filename in iFileList:
         review = filename.split('-')[1]
         if review == '1':
            self.numNegativeDocs += 1
         elif review == '5':
            self.numPositiveDocs += 1
         fileText = self.loadFile(self.trainDir + filename)
         fileToken = self.tokenize(fileText)
         for token in fileToken:
            if review == '1' and token not in string.punctuation:
               if token not in self.negativeReviews:
                  self.negativeReviews[token] = 1
               else:
                  self.negativeReviews[token] += 1
               self.sumNegativeFeatures += 1
            elif review == '5' and token not in string.punctuation:
               if token not in self.positiveReviews:
                  self.positiveReviews[token] = 1
               else:
                  self.positiveReviews[token] += 1
               self.sumPositiveFeatures += 1
         self.save(self.negativeReviews, "negative_reviews.p")
         self.save(self.positiveReviews, "positive_reviews.p")
    
   def classify(self, sText):
      '''Given a target string sText, this function returns the most likely document
      class to which the target string belongs. This function should return one of three
      strings: "positive", "negative" or "neutral".
      '''
      # Calculate -ve and +ve a priori probabilities and the conditional probabilities for
      # each word in file, multiply all probabilities (or sum their respective logs) to get
      # conditional probabilities of classes. Compare them to predict which class.
      negativePrior = float(self.numNegativeDocs)/(self.numNegativeDocs + self.numPositiveDocs)
      positivePrior = float(self.numPositiveDocs)/(self.numNegativeDocs + self.numPositiveDocs)
      negativeConditionalProbability = math.log(negativePrior)
      positiveConditionalProbability = math.log(positivePrior)
      fileToken = self.tokenize(sText)
      for token in fileToken:
         if token not in string.punctuation:
            if token in self.negativeReviews:
               featureNegativeConditionalProbability = float(self.negativeReviews[token] + 1) / (self.sumNegativeFeatures + (1 * (self.numNegativeDocs + self.numPositiveDocs)))
            else:
               featureNegativeConditionalProbability = float(1) / (self.sumNegativeFeatures + 1)
            negativeConditionalProbability += math.log(featureNegativeConditionalProbability)
            if token in self.positiveReviews:
               featurePositiveConditionalProbability = float(self.positiveReviews[token] + 1) / (self.sumPositiveFeatures + (1 * (self.numNegativeDocs + self.numPositiveDocs)))
            else:
               featurePositiveConditionalProbability = float(1) / (self.sumPositiveFeatures + 1)
            positiveConditionalProbability += math.log(featurePositiveConditionalProbability)
      diff = negativeConditionalProbability - positiveConditionalProbability
      if diff > 1:
         return "negative"
      elif diff < -1:
         return "positive"
      else:
         return "neutral"


   def loadFile(self, sFilename):
      '''Given a file name, return the contents of the file as a string.'''

      f = open(sFilename, "r")
      sTxt = f.read()
      f.close()
      return sTxt
   
   def save(self, dObj, sFilename):
      '''Given an object and a file name, write the object to the file using pickle.'''

      f = open(sFilename, "w")
      p = pickle.Pickler(f)
      p.dump(dObj)
      f.close()
   
   def load(self, sFilename):
      '''Given a file name, load and return the object stored in the file.'''

      f = open(sFilename, "r")
      u = pickle.Unpickler(f)
      dObj = u.load()
      f.close()
      return dObj

   def tokenize(self, sText): 
      '''Given a string of text sText, returns a list of the individual tokens that 
      occur in that string (in order).'''

      lTokens = []
      sToken = ""
      for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\'" or c == "_" or c == '-':
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))
               
      if sToken != "":
         lTokens.append(sToken)

      return lTokens

   def calculatePerformance(bc, testDir, trainDir, iFileList):
      results = {"negative":0, "neutral":0, "positive":0}

      bc = Bayes_Classifier(trainDir)
      numTrueNegative = 0
      numTruePositive = 0
      numFalseNegative = 0
      numFalsePositive = 0
      for filename in iFileList:
         fileText = bc.loadFile(testDir + filename)
         result = bc.classify(fileText)
         results[result] += 1
         groundTruth = filename.split('-')[1]
         if result == "negative":
            result = '1'
         elif result == "positive":
            result = '5'
         else:
            result = '0'
         if groundTruth == '1' and result == groundTruth:
            numTrueNegative += 1
         elif groundTruth == '1' and result != groundTruth:
            numFalseNegative += 1
         elif groundTruth == '5' and result == groundTruth:
            numTruePositive += 1
         elif groundTruth == '5' and result != groundTruth:
            numFalsePositive += 1

      print "\nResults Summary:"
      for r in results:
         print "%s: %d" % (r, results[r])
      numTrueTotal = numTruePositive + numTrueNegative
      numFalseTotal = numFalsePositive + numFalseNegative
      # Calculate and return accuracy, precision, and recall
      return (100*(float(numTrueTotal)/(numTrueTotal + numFalseTotal)), 100*(float(numTruePositive)/(numTruePositive + numFalsePositive)), 100*(float(numTruePositive)/(numTruePositive + numFalseNegative)))
      
