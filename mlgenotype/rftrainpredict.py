import sys
import argparse
from mlgenotype import rfgenotype

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Train a random forest model and use it to predict genotypes on real data."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-s', '--simdata', default='./TrainingData.txt', metavar='tab-delimited file of features/genotypes to train on')
    parser.add_argument('-r', '--realdata', default='', metavar='tab-delimited file of features to run fitted predictions on')
    return parser

def main() -> None:
   parser = init_argparse()
   args = parser.parse_args()

   # reads in simulated dataset that will be used to create model for real data
   simdatafile = args.simdata
   print("Simulated data file: " + simdatafile)
   simfeatures, simgenotypes, columnnames, uniquegenos = rfgenotype.read_data_file(simdatafile)
   trainsim_x, testsim_x, trainsim_y, testsim_y = rfgenotype.separate_test_data(simfeatures, simgenotypes)

   # now optimize parameters using GridSearchCV (saving GSCV's best estimator model fit on all the data with the best params)
   grid_sim = rfgenotype.rfgrid(trainsim_x, trainsim_y)
   model_grid =  grid_sim.best_estimator_  # model from grid

   # write out feature importance values:
   importances = model_grid.feature_importances_
   with open('feature_importance_values.txt', 'w') as writer:
      for imp in importances:
         writer.write(str(imp) + '\n')

   # then separately train a model with best params on all the training data:
   best_params_sim = grid_sim.best_params_  # finds best parameters
   cal_score_output_sim = rfgenotype.best_rf_model_and_score(trainsim_x.to_numpy(), trainsim_y.to_numpy(), best_params_sim['n_estimators'], best_params_sim['max_depth'])
   model_sim = cal_score_output_sim[0]  # model from simulated data
   model_sim_scores = cal_score_output_sim[1]
   
   # testing simulated model with 100 test points that were taken out beforehand
   test_preds = model_sim.predict(testsim_x)  # predicting x variables from test set using model
   test_actual = testsim_y
   print("Estimated CV scores for best parameters:")
   print(model_sim_scores)
   print("Accuracy of model recalculated using calculate_score function for predictions on 100 held out test samples:")
   print(rfgenotype.accuracy_score(test_actual, test_preds))

   # testing simulated model with 100 test points that were taken out beforehand
   test_preds = model_grid.predict(testsim_x)  # predicting x variables from test set using model
   print("Accuracy of best estimator model from GridSearchCV on 100 held out test samples:")
   print(rfgenotype.accuracy_score(test_actual, test_preds))

   # reads in real data
   realdatafile = args.realdata
   if realdatafile != '':
      realfeatures, realgenos, realcolumns, realuniquegenos = rfgenotype.read_data_file(realdatafile, shuffle=False)
      y_pred_grid = model_grid.predict(realfeatures.to_numpy())  # finds genotype probability for predictions using model
   
      y_prob_grid = model_grid.predict_proba(realfeatures.to_numpy()) # finds genotype probability for predictions using GridSearchCV

      # creates textfiles to put all predictions/probability predictions in 
      with open('genotype_output_grid.txt', 'w') as writer:
         for index, genotype in enumerate(y_pred_grid):
            writer.write(str(index+1) + ': ' + genotype + '\n')
      with open('genotype_output_grid_probs.txt', 'w') as writer:
         for i in range(len(y_prob_grid)):
            output = y_prob_grid[i]
            writer.write(str(output) + '\n')

if __name__ == "__main__":
    main()
