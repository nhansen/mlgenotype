import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score
import math
import pickle

# reads a file of features and target values, tab-delimited, with one sample per line
def read_data_file(filename_path, shuffle=True):
 
    # reads in dataset
    df = pd.read_csv(filename_path, sep='\t')
    
    # randomly shuffles dataset
    if shuffle:
        df = df.sample(frac=1)
    
    # drops 'Genotype' column from original dataframe, saves 'x' variables
    df_x = df.drop(['Genotype'], axis=1)

    # represents actual mutated genotype for each observation, saves 'y' variables
    df_y = df['Genotype'] 

    # grabs coverage for each chromosomal section (note--this includes 'Genotype' column)
    df_column_names = df.columns
    
    # stores the 6 mutation genotypes in a list
    genotype = df.Genotype.unique()

    return df_x, df_y, df_column_names, genotype

# splits data set, reserving some samples to use as a test set: note that samples should have been shuffled in the read_data_file routine for this to be unbiased separation
def separate_test_data(df_x, df_y, holdoutnum=100):
    # takes 100 random samples out and stores it
    df_variables_test = df_x[:holdoutnum]
    df_output_genotype_test = df_y[:holdoutnum]

    # keeps rest of variables not taken out to train model
    df_variables_train = df_x[holdoutnum:]
    df_output_genotype_train = df_y[holdoutnum:]
    
    return df_variables_train, df_variables_test, df_output_genotype_train, df_output_genotype_test

# finds best parameters using GridSearchCV
def rfgrid(df_x, df_y):
    limit = int(math.log2(len(df_x.index)))

    n_trees = [100, 200, 300, 400, 500]
    max_dep = [2, 3, 4, 5, 6, 7, 8, 9, 10]

    if (limit in max_dep) == False:
        for m in max_dep:
            if limit < m:
                max_dep.insert(max_dep.index(m), limit)
                break

    if max_dep[-1] < limit:
        max_dep.append(limit)
    
    parameters = {'n_estimators':n_trees, 'max_depth':max_dep}
    
    rf_grid = GridSearchCV(RandomForestClassifier(random_state=2), param_grid=parameters,
                          return_train_score=True, cv=5)
    rf_grid.fit(df_x, df_y)
    
    return rf_grid


# calculates cross validation score of an RF model with default hyper parameters
# ALSO returns model created. BUT can also just use .best_estimator from GridSearchCV
# tutorial referenced:
### https://www.youtube.com/watch?v=gJo0uNL-5Qw
def best_rf_model_and_score(featuredf, genos, best_n_trees, best_max_depth):

    model = RandomForestClassifier(n_estimators=best_n_trees, max_depth=best_max_depth,
                                       random_state=2)
    model.fit(featuredf, genos)

    cross_score = cross_val_score(model, featuredf, genos, cv=5)
    
    return model, cross_score

def save_model_to_file(fittedmodel, filename):

    pickle.dump(fittedmodel, open(filename, 'wb'))

def load_model_from_file(filename):

    loaded_model = pickle.load(open(filename, 'rb'))

    return loaded_model

