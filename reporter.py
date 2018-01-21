import os
import numpy as np
from logger import *
import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description=None)

    parser.add_argument("--trg", default="",
                        help="target file for evaluation score of each population")
    parser.add_argument("--scr", default="", help="score file")

    parser.add_argument("--pop", default=30, type=int, help="population")
    parser.add_argument("--n-pop", type=int, help="current population index")
    parser.add_argument("--n-gen", type=int, help="current generation index")

    args = parser.parse_args()
    return args


def read_scr_file(args):
    with open(args.scr) as f:
        scores_raw = f.readlines()

    scores = list(map(lambda x: [x.split()[3][:-1]] +
                      x.split()[4].split("/"), scores_raw))

    logging.info("File: %s, # of evaluation records: %s" %
                 (args.scr, len(scores)))
    return np.array(scores)


def report(args, rst):
    try:
        with open(args.trg, "r") as f:
            scores = f.readlines()
    except:
        logging.info("Creating new file: " + args.trg)
        # os.system("touch " + args.trg)
        scores = []

    with open(args.trg, "w") as f:
        scores = scores + [str(args.n_pop).zfill(2) + "\t" + str(rst) + "\n"]
        logging.info("collecting: %s" % scores[-1][:-1])
        logging.info("# of collected score: %s" % len(scores))
        scores = sorted(scores)
        f.writelines(scores)
        f.flush()

    if len(scores) == args.pop:
        logging.info(
            "Collected evulation result of all population. start next generation...")
        os.system("./run.sh %s" % (args.n_gen + 1))


if __name__ == "__main__":
    args = get_arguments()
    scores = read_scr_file(args)
    report(args, scores[-1][0])
