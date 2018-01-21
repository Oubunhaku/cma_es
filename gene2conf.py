from template import BaseTemplate
import numpy as np
import os
from logger import *
import argparse


# target_path = "generation_%s/model_description/"
# target_file = "model_%s.conf"
# genes_path = "generation_00/genes/"
hparams = [
    "batch_size",
    "rnn_num_hidden",
    "num_layers",
]
map_funcs = [
    lambda x: np.ceil(x).astype(np.int),
    lambda x: np.floor(x).astype(np.int),
    lambda x: np.ceil(x + 100).astype(np.int),
]
# generation = 0

assert len(hparams) == len(map_funcs)


def get_arguments():
    parser = argparse.ArgumentParser(description=None)

    parser.add_argument("--trg", default="",
                        help="path to generated model description file")
    parser.add_argument("--gene-path", default="", help="path to gene folder")

    parser.add_argument("--n-gen", type=int, help="current generation index")
    args = parser.parse_args()
    return args


def gene_parser(args):
    gene_files = sorted(os.listdir(args.gene_path))
    genes = []

    for gene_file in gene_files:
        with open(args.gene_path + gene_file) as f:
            gene = f.readlines()
        gene = list(map(lambda x: float(x.strip()), gene))
        genes.append(gene)

    # return a matrix with shape (num_gene, num_target_hparam)
    return np.array(genes)


def decode(param, gene):
    # add rule here
    return str(gene)


def decoder(hparams, genes, map_funcs):
    for gene_idx in range(genes.shape[1]):
        genes[:, gene_idx] = map_funcs[gene_idx](genes[:, gene_idx])

    for gene in genes:
        updated_hparams = dict()
        for i, hparam in enumerate(hparams):
            updated_hparams[hparam] = decode(hparam, gene[i])
        yield updated_hparams


if __name__ == "__main__":
    args = get_arguments()
    genes = gene_parser(args)

    base = BaseTemplate()
    logging.info("======================================================")
    logging.info("(Generation %d) Start generate model description" % args.n_gen)
    logging.info("======================================================")

    for idx, updated_hparam in enumerate(decoder(hparams, genes, map_funcs)):
        base.update(updated_hparam)
        sample = base.render()
        with open(args.trg % str(idx).zfill(2), "w") as f:
            f.writelines(sample)
            f.flush()
        logging.info("Generating model description file for Model: %s, Generation: %s -> %s" % (
            idx, args.n_gen, args.trg % str(idx).zfill(2)))
