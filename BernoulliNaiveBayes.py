##########################
# BERNOULLI NAIVE BAYESS #
##########################
#%%
import pandas as pd

from sklearn.naive_bayes import BernoulliNB
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer

%matplotlib inline

#%%
#Read entire dataset in a panda DataFrame
dataset = pd.read_json('./Dataset/Toys_and_Games_5.json',lines=True)
dataset

#%%
#Let’s take a look at the distribution of scores across reviews
dataset['overall'].value_counts().plot(kind='bar', color='cornflowerblue')

#%%
#Split dataset into test and training data.
X_train, X_test, y_train, y_test = train_test_split(dataset['reviewText'],
                                                   dataset['overall'],
                                                   test_size=0.2, random_state=1)

#%%
#Feature extraction:
#represent each review as a feature vectore for BERNOULLI NAIVE BAYES MODEL
#Use the BAG OF WORD representation.
#Tokenize train and test data
#CountVectorizer implements both tokenization and occurrence counting in a single class.
#Count Vector is a matrix notation of the dataset in which every row represents a document 
#from the corpus, every column represents a term from the corpus, and every cell 
#represents the frequency count of a particular term in a particular document.
#It also possible to perform binary count(1 if the word occour in a particular document,
#0 otherwise) for Bernoully bayes model.
vect = CountVectorizer(binary=True)

X_train_dtm = vect.fit_transform(X_train) #Learn the vocabulary dictionary and return term-document matrix.
print("number words in training corpus:", len(vect.get_feature_names()))
X_test_dtm = vect.transform(X_test) #Transform documents to document-term matrix.

#%%
#Instantiate and train a bernoulli naive Bayes model.
nb = BernoulliNB()
nb.fit(X_train_dtm, y_train)

#%%
#Make class predictions
y_pred = nb.predict(X_test_dtm)

#%%
#Calculate accuracy, precision, recall, and F-measure of class predictions
def eval_predictions(y_test, y_pred):
    print('accuracy:', metrics.accuracy_score(y_test, y_pred))
    print('precision:', metrics.precision_score(y_test, y_pred, average='weighted'))
    print('recall:', metrics.recall_score(y_test, y_pred, average='weighted'))
    print('F-measure:', metrics.f1_score(y_test, y_pred, average='weighted'))

eval_predictions(y_test, y_pred)

#%%
#Take a look at examples where the model is getting it wrong.
# print message text for the first 3 false positives
print('False positives:')
print()
for x in X_test[y_test < y_pred][:2]:
    print(x)
    print()

# print message text for the first 3 false negatives
print('False negatives:')
print()
for x in X_test[y_test > y_pred][:2]:
    print(x)
    print()
#%%
