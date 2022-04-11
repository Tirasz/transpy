from pathlib import Path
import os
import subprocess

TEST_FILES_PATH = Path("./test_files").resolve()
REFERENCE_FILES_PATH = Path("./reference_files").resolve()
TRANSFORMED_FILES_PATH = Path("./transformed-test_files").resolve()


def main():
    test_files = [f for f in TEST_FILES_PATH.rglob('*.py')]
    reference_files = [f for f in REFERENCE_FILES_PATH.rglob('*.py')]

    if len(test_files) > len(reference_files):
        diff = list(set([os.path.basename(f.name) for f in test_files]).symmetric_difference(set([os.path.basename(f.name) for f in reference_files])))
        print(f"MISSING REFERENCE FILES FOR: {diff}")
        return

    subprocess.run(["python","../../transpy",f"{TEST_FILES_PATH}", "-o"])

    tr_log_file = TRANSFORMED_FILES_PATH / 'transpy-output/transformer.log'

    if tr_log_file.exists():
        with open(TRANSFORMED_FILES_PATH / 'transpy-output') as f:
            lines = f.readlines()
        for line in lines:
            if "REVERTING" in line:
                print("TRANSFORMATION CAUSED A SYNTAX ERROR! CHECK LOGS!")
            elif "SyntaxError" in line:
                print("SYNTAX ERROR IN TEST FILE! CHECK LOGS!")
    
    transformed_files = [f for f in TRANSFORMED_FILES_PATH.rglob('*.py')]

    for tr_file in transformed_files:
        name = os.path.basename(tr_file.name)
        rf_file = REFERENCE_FILES_PATH / name
        with open(tr_file, 'r') as tr, open(rf_file, 'r') as rf:
            tlines = tr.readlines()
            rlines = rf.readlines()
            l = len(rlines)
            if len(rlines) != len(tlines):
                print(f"LINES FOR {name} ARE DIFFERENT IN REFERENCE AND TEST FILE!")
                return
            for i in range(l):
                if tlines[i] != rlines[i]:
                    print(f"[{name}]: DIFFERENCE AT LINE ({i+1})!")


if __name__ == "__main__":
    main()