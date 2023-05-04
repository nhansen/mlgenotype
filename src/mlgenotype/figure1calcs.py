import sys
import argparse
from mlgenotype import rfgenotype

def init_argparse() -> argparse.ArgumentParser:
     parser = argparse.ArgumentParser(
         usage="%(prog)s [OPTION] [FILE]...",
         description="Generate data for the manuscript."
     )
     parser.add_argument(
         "-v", "--version", action="version",
         version = f"{parser.prog} version 1.0.0"
     )
     parser.add_argument('-r', '--train', default='training_data.txt', metavar='file of sample k-mer counts with one sample per line and tab-delimited feature values for each sample. File should contain a header, and the final field of each line should be the genotype')
     parser.add_argument('-t', '--test', default='training_data.txt', metavar='file of sample k-mer counts with one sample per line and tab-delimited feature values for each sample. File should contain a header, and the final field of each line should be the genotype')
     parser.add_argument('-o', '--outdir', default='rfresults', metavar='directory for output files. Subdirectory models will have saved models, and subdirectory predictions will have the predictions of those models')
     parser.add_argument('-p', '--prefix', default='rfresults', metavar='prefix for output filenames')
 
     return parser

def main() -> None:

    parser = init_argparse()
    args = parser.parse_args()
 
    # Number of training samples to use:
    ntrainvals = [110, 220, 441, 882, 1764, 2646]
    #ntrainvals = [5292]
 
    # reads in simulated dataset that will be used to train our RF models, shuffling:
    traindatafile = args.train
    trainsim_x, trainsim_y, traincolumnnames, trainuniquegenos = rfgenotype.read_data_file(traindatafile, shuffle=True)
 
    # reads in simulated dataset that will be used to test our RF models, without shuffling:
    testdatafile = args.test
    testsim_x, testsim_y, testcolumnnames, testuniquegenos = rfgenotype.read_data_file(testdatafile, shuffle=False)
 
    for ntrain in ntrainvals:
        # pull out ntrain samples for training our model:
        holdout = len(trainsim_x) - ntrain
        train_x, test_x, train_y, test_y = rfgenotype.separate_test_data(trainsim_x, trainsim_y, holdoutnum=holdout)
        if len(train_x) != ntrain:
            print("train_x length is not as expected!")
            trainxlength = len(train_x)
            print("train_x length: " + str(trainxlength) + " holdout: " + str(holdout))
            sys.exit(1)
  
        # optimize hyperparameters using GridSearchCV:
        grid_sim = rfgenotype.rfgrid(train_x, train_y)
        best_params_sim = grid_sim.best_params_  # best hyperparameters
        rf_model =  grid_sim.best_estimator_  # model fit with all data and best hyperparameters
        best_params_score = grid_sim.best_score_ # mean CV score of model fit with all data and best hyperparameters
  
        # report where output will go:
        outputbase = args.prefix
        print("Writing model to " + outputbase + "." + str(ntrain) + ".rf.model, model accuracy stats to " + outputbase + "." + str(ntrain) + ".rf.stats, and feature importance values to " + outputbase + "." + str(ntrain) + ".rf.importance.txt in models directory" )
  
        # save the optimized model to <outputbase>.rf.model:
        rfgenotype.save_model_to_file(rf_model, args.outdir + "/models/" + outputbase + "." + str(ntrain) + ".rf.model")
  
        # write out feature importance values:
        importances = rf_model.feature_importances_
        importancefile = args.outdir + "/models/" + outputbase + "." + str(ntrain) + ".rf.importance.txt"
        with open(importancefile, 'w') as impwriter:
            for imp in importances:
                impwriter.write(str(imp) + '\n')
     
        statsfile = args.outdir + "/models/" + outputbase + "." + str(ntrain) + ".rf.stats"
        with open(statsfile, 'w') as statswriter:
            statswriter.write("RF model best hyperparameters:\nBest number of estimators: " + str(best_params_sim['n_estimators']) + "\nBest maximum depth: " + str(best_params_sim['max_depth']) + "\n")
            statswriter.write("RF model mean CV score (all data, best hyperparameters):\n" + str(best_params_score) + "\n")
  
        # now test this model with the appropriate test data and print results:
        test_preds = rf_model.predict(testsim_x.to_numpy())
        test_probs = rf_model.predict_proba(testsim_x.to_numpy())
        actual_genos = testsim_y
        modelpredfile = args.outdir + "/predictions/" + outputbase + "." + str(ntrain) + ".rf.genotypes.txt"
        with open(modelpredfile, 'w') as predwriter:
            for i in range(len(test_preds)):
                probs = test_probs[i]
                maxprob = max(probs) 
                predwriter.write(str(i + 1) + "\t" + str(test_preds[i]) + "\t" + str(actual_genos[i]) + "\t" + str(maxprob) + "\n")
   
if __name__ == "__main__":
    main()
