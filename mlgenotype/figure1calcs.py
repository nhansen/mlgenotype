import sys
import os
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
     parser.add_argument('-r', '--train', required=True, metavar='Training file of sample k-mer counts with one sample per line and tab-delimited feature values for each sample. File should contain a header, and the final field of each line should be the genotype')
     parser.add_argument('-t', '--test', required=False, metavar='Test file of sample k-mer counts with one sample per line and tab-delimited feature values for each sample. File should contain a header, and the final field of each line should be the genotype. If no test file is specified, results for held out training data will be reported.')
     parser.add_argument('-o', '--outdir', default='rfresults', metavar='directory for output files. Subdirectory models will have saved models, and subdirectory predictions will have the predictions of those models')
     parser.add_argument('-p', '--prefix', default='rfresults', metavar='prefix for output filenames')
 
     return parser

def main() -> None:

    parser = init_argparse()
    args = parser.parse_args()
 
    # Number of training samples to use:
    ntrainvals = [60, 120, 180, 240, 300, 360]
 
    # reads in simulated dataset that will be used to train our RF models, shuffling:
    traindatafile = args.train
    trainsim_x, trainsim_y, traincolumnnames, trainuniquegenos = rfgenotype.read_data_file(traindatafile, shuffle=True)
 
    # if a test file is specified, reads in simulated dataset that will be used to test our RF models, without shuffling:
    if args.test:
        testdatafile = args.test
        testsim_x, testsim_y, testcolumnnames, testuniquegenos = rfgenotype.read_data_file(testdatafile, shuffle=False)
 
    # create directories if necessary:
    if not os.path.exists(args.outdir):
        os.makedirs(args.outdir)
    if not os.path.exists(args.outdir + "/models"):
        os.makedirs(args.outdir + "/models")
    if not os.path.exists(args.outdir + "/predictions"):
        os.makedirs(args.outdir + "/predictions")

    # open a file to write the accuracy results:
    accuracyfile = args.outdir + "/accuracy.txt"
    acc_fh = open(accuracyfile, 'w')

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
        #print("Writing model to " + outputbase + "." + str(ntrain) + ".rf.model, model accuracy stats to " + outputbase + "." + str(ntrain) + ".rf.stats, and feature importance values to " + outputbase + "." + str(ntrain) + ".rf.importance.txt in models directory" )

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
        if args.test:
            testdata_x = testsim_x.to_numpy()
            actual_genos = testsim_y
        else:
            testdata_x = test_x.values[0:100]
            actual_genos = test_y.values[0:100]
        test_preds = rf_model.predict(testdata_x)
        test_probs = rf_model.predict_proba(testdata_x)
        modelpredfile = args.outdir + "/predictions/" + outputbase + "." + str(ntrain) + ".rf.genotypes.txt"
        predcorrect = 0
        predtotal = 0
        with open(modelpredfile, 'w') as predwriter:
            for i in range(len(test_preds)):
                probs = test_probs[i]
                maxprob = max(probs) 
                if test_preds[i] == actual_genos[i]:
                    predcorrect = predcorrect + 1
                predtotal = predtotal + 1
                predwriter.write(str(i + 1) + "\t" + str(test_preds[i]) + "\t" + str(actual_genos[i]) + "\t" + str(maxprob) + "\n")
        predacc = 1.0*predcorrect/predtotal
        acc_fh.write(str(ntrain) + "\t" + str(best_params_score) + "\t" + str(predacc) + "\n")
    acc_fh.close()
   
if __name__ == "__main__":
    main()
