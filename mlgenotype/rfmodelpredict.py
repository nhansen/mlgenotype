import sys
import argparse
from mlgenotype import rfgenotype
import warnings
from sklearn.exceptions import DataConversionWarning

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [FILE]...",
        description="Use a trained random forest model to predict genotypes and probabilities for a feature set."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-m', '--modelfile', metavar='pickle file with RF model to load, as created by RFModelTrain.py', required=True)
    parser.add_argument('-f', '--featurefile', metavar='tab-delimited file of validation features/genotypes on which to predict genotypes', required=True)
    parser.add_argument('-o', '--outputfilebase', default='model', metavar='filename base for output files. Genotypes will be written to <filebase>.rf.genos, probabilities to <filebase>.rf.probs')

    return parser

def main() -> None:
   parser = init_argparse()
   args = parser.parse_args()

   warnings.filterwarnings(action='ignore', category=UserWarning)

   # load the optimized model specified with the --modelfile argument:
   modelfile = args.modelfile
   rf_model = rfgenotype.load_model_from_file(modelfile)
   print("Using RF model loaded from file: " + modelfile)

   # reads in feature dataset that will be used for making predictions with the RF model:
   featurefile = args.featurefile
   print("Using RF model to make predictions from features in file: " + featurefile)

   # report where output will go:
   outputbase = args.outputfilebase
   print("Will write genotypes to " + outputbase + ".rf.genos, genotype probabilities to " + outputbase + ".rf.probs")

   data_x, data_y, columnnames, uniquegenos = rfgenotype.read_data_file(featurefile, shuffle=False)
   data_preds = rf_model.predict(data_x.to_numpy())  # predicting y variables from feature set using model
   data_probs = rf_model.predict_proba(data_x.to_numpy())  # predicted probabilities for different genotypes

   # creates textfiles to put all predictions/probability predictions in 
   with open(outputbase + '.rf.genos', 'w') as writer:
      for index, genotype in enumerate(data_preds):
         output = data_probs[index]
         maxprob = max(output)
         writer.write(str(index+1) + '\t' + genotype + '\t' + str(maxprob) + '\n')
   writer.close()
   #with open(outputbase + '.rf.probs', 'w') as writer:
      #for i in range(len(data_probs)):
         #output = data_probs[i]
         #maxprob = max(output)
         ##writer.write(str(output) + '\n')
         #writer.write(str(maxprob) + '\n')
   #writer.close()


if __name__ == "__main__":
    main()
