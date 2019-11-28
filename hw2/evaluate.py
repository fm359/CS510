testFile = "bayes.py"
trainDir = "movies_reviews/"

execfile(testFile)
bc = Bayes_Classifier(trainDir)

testDir = sys.argv[1]
iFileList = []

for fFileObj in os.walk(testDir):
	iFileList = fFileObj[2]
	break
print '%d test reviews.' % len(iFileList)

(accuracy, precision, recall) = bc.calculatePerformance(testDir, trainDir, iFileList)
fMeasure = (2 * precision * recall) / (precision + recall)
print ("Classification Accuracy:  %.2f%%" % accuracy)
print ("Classification Precision: %.2f%%" % precision)
print ("Classification Recall:    %.2f%%" % recall)
print ("Classification F-measure: %.2f%%" % fMeasure)
