# current generation
n_generation=$1
# number of generation 
generation=2
# current population
n_population=0
# number of population
population=30
# path to checkpoint folder
checkpoint_path="checkpoints/"
# checkpoint files
checkpoint="${checkpoint_path}es_G%s.pkl"
# path to current generation folder
generation_path="generation_$(printf "%02d" "$n_generation")/"
# path to previous generation folder
prev_generation_path="generation_$(printf "%02d" "`expr $n_generation - 1`")/"
# path to current genes folder
gene_path="${generation_path}genes/"
# path to gene files
gene="${gene_path}/%s.gene"
# initial gene file
init="gene.init"
# path for model description file's folder
model_desc_path="${generation_path}model_description/"
# path to model descption file 
model_desc="${model_desc_path}model_%s.conf"
# model folder
model_path="${generation_path}model_$(printf "%02d" "$n_population")/"
# path to evaluation score path
eval_scr="${model_path}bleu.scr"
# number of hyperparameter to be optimized
n_hparam=5

# command for python interpreter
py_cmd=python3

if(($n_generation>=$generation)) 
then
  exit 
fi

if [ ! -d $checkpoint_path ]; then
  mkdir $checkpoint_path
fi


# generate genes for current generation
# create some necessary folder
mkdir $generation_path
mkdir $gene_path
$py_cmd evo_single.py \
--checkpoint $checkpoint \
--gene $gene \
--init $init \
--scr ${prev_generation_path}genes.scr \
--pop $population \
--n-pop $n_population \
--n-gen $n_generation 

# generate model description file for genes in current generation
# create some necessary folder
mkdir $model_desc_path
$py_cmd gene2conf.py \
--trg $model_desc \
--gene-path $gene_path \
--n-gen $n_generation
    

# submit each task depends on model description file
for ((n_population=0;n_population<$population;n_population++))
  do
    model_path="${generation_path}model_$(printf "%02d" "$n_population")/"
    mkdir $model_path
    touch ${eval_scr}
    
    $py_cmd toy_nmt.py \
    --model-desc $model_desc \
    --trg $eval_scr \
    --n-gen $n_generation \
    --n-model $n_population

    # report result
    $py_cmd reporter.py \
    --trg ${generation_path}genes.scr \
    --scr $eval_scr \
    --pop $population \
    --n-pop $n_population \
    --n-gen $n_generation

  done    

echo "Finished!"
