import cma
import numpy as np
import pickle
import os
import argparse
from logger import *

# generation = 10
# population = 30

# backup = "backup_files/"
# init_hparam = "protos/gene_cont"
# score_file = ""
# es_filename = "es_generation_%s.pkl"
# gene_vec_filename = "gene_vec_%s.pkl"
# gene_path = "generation_%s/genes"
# gene_file = "generation_%s/genes/%s.gene"


def get_arguments():
    parser = argparse.ArgumentParser(description=None)

    parser.add_argument("--checkpoint", default="checkpoints/es_G%s.pkl",
                        help="path to checkpoint files")
    parser.add_argument("--gene", default="generation_%s/genes/%s.gene",
                        help="path to backup es files")
    parser.add_argument("--init", default="gene.init", help="init gene file")
    parser.add_argument("--scr", default="", help="path to score file")

    parser.add_argument("--pop", default=30, type=int, help="population")
    parser.add_argument("--n-pop", type=int, help="current population index")
    parser.add_argument("--n-gen", type=int, help="current generation index")
    args = parser.parse_args()
    return args


def evolution(args):
    logging.info("======================================================")
    logging.info("(Generation %d) Start generating genes..." % args.n_gen)
    logging.info(args)
    logging.info("======================================================")
    if args.n_gen == 0:
        with open(args.init) as f:
            init_vec = f.readlines()
        init_vec = list(map(lambda x: float(x.strip()), init_vec))

        es = cma.CMAEvolutionStrategy(init_vec, 0.1, {
            'seed': 1,
            'popsize': args.pop,
        })
        X = es.ask()

    else:
        # load previous checkpoint
        with open(args.checkpoint % str(args.n_gen - 1).zfill(2), "rb") as es_file:
            es = pickle.load(es_file)

        X = es.ask()
        # open score file
        with open(args.scr) as f:
            # read score file
            scores = f.readlines()
        Y = list(map(lambda x: float(x.split("\t")[-1].strip()), scores))
        es.tell(X, Y)

    # save current checkpoint
    with open(args.checkpoint % str(args.n_gen).zfill(2), "wb") as es_file:
        pickle.dump(es, es_file)

    for gene_idx in range(args.pop):
        with open(args.gene % str(gene_idx).zfill(2), "w") as gene:
            gene.write("\n".join(X[gene_idx].astype(np.str)))


if __name__ == "__main__":
    args = get_arguments()
    evolution(args)
    logging.info("Generated %s genes." % args.pop)
