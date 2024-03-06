import pandas as pd
import numpy as np
from collections import Counter
import time

personality_df = pd.read_csv('16P.csv',encoding='latin1')
personality_df = personality_df.drop(columns='Response Id')

personality_types_dic = {
'ESTJ': 0,
'ENTJ': 1,
'ESFJ': 2,
'ENFJ': 3,
'ISTJ': 4,
'ISFJ': 5,
'INTJ': 6,
'INFJ': 7,
'ESTP': 8,
'ESFP': 9,
'ENTP': 10,
'ENFP': 11,
'ISTP': 12,
'ISFP': 13,
'INTP': 14,
'INFP': 15}

personality_df = personality_df.replace(personality_types_dic)

personality_np = np.array(personality_df)


# 5-fold cross validation
def fold_cross(array,nth_fold):
    nth_fold -= 1
    splittedarrs = (np.array_split(array, 5))
    chosen_arr = splittedarrs[nth_fold] #test case
    
    if nth_fold == 0:
        secondpart = np.concatenate(splittedarrs[nth_fold+1:])
        rest_arr = secondpart
    elif nth_fold == 4:
        firstpart = np.concatenate(splittedarrs[:nth_fold])
        rest_arr = firstpart
    else:
        firstpart = np.concatenate(splittedarrs[:nth_fold])
        secondpart = np.concatenate(splittedarrs[nth_fold+1:])
        rest_arr = np.concatenate((firstpart,secondpart)) # train case

    x_train, y_train = rest_arr[:,:60], rest_arr[:,-1]
    x_test, y_test = chosen_arr[:,:60], chosen_arr[:,-1]
    return x_train,y_train,x_test,y_test


def compute_distances_no_loops(x_train,x_test):
    x2 = np.sum(np.square(x_test), axis=1)
    y2 = np.sum(np.square(x_train), axis=1)
    dot_product = 2 * np.dot(x_test, x_train.T)
    dists = np.sqrt(x2[:, np.newaxis] - dot_product + y2)
    return dists

def knn(X_train, y_train, x_test, k):
    distances = compute_distances_no_loops(X_train,x_test)
    nearest_indices = np.argsort(distances)
    nearest_labels = y_train[nearest_indices[:,:k]]
    def most_common(arr):
        return Counter(arr).most_common()[0][0]
    prediction = np.apply_along_axis(most_common,1,nearest_labels)
    return prediction



def accuracy(y_true, y_pred):
    return np.mean(y_true == y_pred)

def precision(y_true, y_pred):
    true_positives = np.sum(np.logical_and(y_pred == y_true, y_pred == 1), axis=0)
    false_positives = np.sum(np.logical_and(y_pred != y_true, y_pred == 1), axis=0)
    return true_positives / (true_positives + false_positives)


def recall(y_true, y_pred):
    true_positives = np.sum(np.logical_and(y_pred == y_true, y_pred == 1), axis=0)
    false_negatives = np.sum(np.logical_and(y_pred != y_true, y_true == 1), axis=0)
    return true_positives / (true_positives + false_negatives)




for i in range(1,6):
    print('-----')
    print(f'fold number {i}')
    
    personality_numbers_train, personality_type_train, personality_numbers_test,personality_type_test = fold_cross(personality_np,i)
    for j in [1,3,5,7,9]:
        start_time = time.time()
        k=j
        predicted = knn(personality_numbers_train,personality_type_train,personality_numbers_test,k)
        # true labels
        y_true = personality_type_test
        # predicted labels
        y_pred = predicted


        acc = accuracy(y_true, y_pred)
        prec = precision(y_true, y_pred)
        rec = recall(y_true, y_pred)
        print(f'k is {j}')
        print("Accuracy: ", acc)
        print("Precision: ", prec)
        print("Recall: ", rec)
        print("--- %s seconds ---" % (time.time() - start_time))
    

print("--- %s seconds ---" % (time.time() - start_time))