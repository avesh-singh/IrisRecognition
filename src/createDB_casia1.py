import argparse
import os
from glob import glob
from tqdm import tqdm
from time import time
from scipy.io import savemat
from multiprocessing import cpu_count, Pool
from utils.extractandenconding import extractFeature
from itertools import repeat

# creating a pool function to use with multiprocessing
def pool_func(file, template_dir):
    # print("args", file, template_dir)
    template, mask, _ = extractFeature(file, multiprocess=False)
    basename = os.path.basename(file)
    out_file = os.path.join(template_dir, "%s.mat" % (basename))
    savemat(out_file, mdict={'template': template, 'mask': mask})


if __name__ == '__main__':
    # parsing args from the terminal
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_dir", type=str, default="../CASIA1/*",
                        help="Directory of the dataset")
    parser.add_argument("--template_dir", type=str, default="./templates/CASIA1/",
                        help="Destination of the features database")
    parser.add_argument("--number_cores", type=int, default=cpu_count(),
                        help="Number of cores used in the matching.")
    args = parser.parse_args()

    # time it
    start = time()
    if not os.path.exists(args.template_dir):
        print("makedirs", args.template_dir)
        os.makedirs(args.template_dir)

    files = glob(os.path.join(args.dataset_dir, "*_1_*.jpg"))
    n_files = len(files)
    print("N# of files which we are extracting features", n_files)
    # extracting features using multiple cores (number_cores)
    pools = Pool(processes=args.number_cores)
    for _ in tqdm(pools.starmap(pool_func, zip(files, repeat(args.template_dir))), total=n_files):
        pass
    # total time
    end = time()
    print('\nTotal time: {} [s]\n'.format(end-start))