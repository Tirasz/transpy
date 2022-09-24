import ast
from copy import deepcopy
from analyzer import Transformer, make_output_folder, transform_helper, init_output
from analyzer.utils import OutputHandler
import os, glob
import argparse
import shutil
from pathlib import Path
import concurrent.futures 
import threading
from tqdm import tqdm
import time


from flask import Flask
from flask import render_template
app = Flask(__name__)

    

@app.route('/')
def editor():
    return render_template('editor.html')

if __name__ == "__main__":
    app.run()