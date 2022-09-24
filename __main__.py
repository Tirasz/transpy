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
from flask import request
import json

app = Flask(__name__)


@app.route('/transform', methods = ['POST'])
def asd():
    data = json.loads(request.data)

    try:
        tree = ast.parse(data['code'])
        #print(ast.dump(tree))
        transformer = Transformer()
        transformer.visit(tree)
        result = {'result': ast.unparse(tree)}
    except SyntaxError:
        result = {'result': '#Invalid syntax in source code!'}
    except UnicodeDecodeError:
        result = {'result': '#Invalid characters in source code!'}


    
    return json.dumps(result)

@app.route('/')
def editor():
    return render_template('editor.html')

if __name__ == "__main__":
    app.run()