import sys
import argparse
from mlgenotype import rfgenotype

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Train a random forest model and write it and its accuracy stats out to the file system."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-s', '--simdata', metavar='tab-delimited file of features/genotypes to train on', required=True)
    parser.add_argument('-t', '--testdata', metavar='tab-delimited file of validation features/genotypes on which to measure the models accuracy (optional).')
    parser.add_argument('-o', '--outputfilebase', default='model', metavar='filename base for output files. Model will be written to <filebase>.model, accuracy statistics to <filebase>.stats')

    return parser

def main() -> None:
   parser = init_argparse()
   args = parser.parse_args()

   # reads in simulated dataset that will be used to fit our RF model:
   simdatafile = args.simdata
   print("Training with simulated data file: " + simdatafile)

   # if data for validating the fitted model exists, read that in:
   valdatafile = args.testdata
   testsim_x = None
   if valdatafile is not None:
       print("Checking fitted models accuracy with data in file: " + valdatafile)
       testsim_x, testsim_y, testcolumnnames, testuniquegenos = rfgenotype.read_data_file(valdatafile, shuffle=False)

   # report where output will go:
   outputbase = args.outputfilebase
   print("Will write model to " + outputbase + ".rf.model, model accuracy stats to " + outputbase + ".rf.stats, and feature importance values to " + outputbase + ".rf.importance.txt")

   trainsim_x, trainsim_y, traincolumnnames, trainuniquegenos = rfgenotype.read_data_file(simdatafile)

   # now optimize parameters using GridSearchCV (saving GSCV's best estimator model fit on all the data with the best params)
   grid_sim = rfgenotype.rfgrid(trainsim_x, trainsim_y)
   best_params_sim = grid_sim.best_params_  # finds best parameters
   rf_model =  grid_sim.best_estimator_  # model fit with all data and best hyperparameters
   best_params_score = grid_sim.best_score_ # mean CV score of model fit with all data and best hyperparameters

   # save the optimized model to <outputbase>.rf.model:
   rfgenotype.save_model_to_file(rf_model, outputbase + ".rf.model")

   # write out feature importance values:
   importances = rf_model.feature_importances_
   importancefile = outputbase + ".rf.importance.txt"
   with open(importancefile, 'w') as impwriter:
      for imp in importances:
         impwriter.write(str(imp) + '\n')

   statsfile = outputbase + ".rf.stats"
   with open(statsfile, 'w') as statswriter:
      statswriter.write("RF model best hyperparameters:\nBest number of estimators: " + str(best_params_sim['n_estimators']) + "\nBest maximum depth: " + str(best_params_sim['max_depth']) + "\n")
      statswriter.write("RF model mean CV score (all data, best hyperparameters):\n" + str(best_params_score) + "\n")

      # testing simulated model with validation samples, if they were provided
      if testsim_x is not None:
         test_preds = rf_model.predict(testsim_x)  # predicting x variables from validation set using model
         test_actual = testsim_y
         print("Accuracy of fitted RF model for held out validation set:")
         test_accuracy = rfgenotype.accuracy_score(test_actual, test_preds)
         statswriter.write(str(test_accuracy) + "\n")

if __name__ == "__main__":
    main()
