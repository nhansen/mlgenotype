import pytest
import subprocess
import sys

def test_predict():
    subprocess.check_call([sys.executable, '-m' 'rfmodelpredict'])
