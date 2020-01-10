# gnomAD Python API by @furkanmtorun 
# [furkanmtorun@gmail.com](mailto:furkanmtorun@gmail.com) 
# | GitHub: [@furkanmtorun](https://github.com/furkanmtorun)  
# | [Google Scholar](https://scholar.google.com/citations?user=d5ZyOZ4AAAAJ) 
# | [Personal Website](https://furkanmtorun.github.io/)

# Import required libraries and packages
from pandas.io.json import json_normalize as json_normalize
from tqdm import tqdm
import pandas as pd
import requests
import argparse
import json
import os

# Create a folder for outputs in the current directory
if not os.path.exists('outputs/'):
    os.mkdir('outputs/')

# Argument parsing
def arg_parser():
    global filter_by
    global search_by
    global dataset
    parser = argparse.ArgumentParser()
    parser.add_argument("-filter_by", type=str, required=True, default="gene_name", help="Get your variants according to: gene_name, gene_id or transcript_id ")
    parser.add_argument("-search_by", type=str, required=True, default="TP53", help="Type the Ensembl Gene ID or Gene Name or the file name (e.g: myGenes.txt) containing genes")
    parser.add_argument("-dataset", type=str, required=True, default="gnomad_r2_1", help="Select your dataset: exac, gnomad_r2_1, gnomad_r3, gnomad_r2_1_controls, gnomad_r2_1_non_neuro, gnomad_r2_1_non_cancer, gnomad_r2_1_non_topmed")
    args = parser.parse_args()
    if args.dataset not in ["exac", "gnomad_r2_1", "gnomad_r3", "gnomad_r2_1_controls", "gnomad_r2_1_non_neuro", "gnomad_r2_1_non_cancer", "gnomad_r2_1_non_topmed"]:
        print("! Select a proper gnomAD data set:\n\texac, gnomad_r2_1, gnomad_r3, gnomad_r2_1_controls, gnomad_r2_1_non_neuro, gnomad_r2_1_non_cancer, gnomad_r2_1_non_topmed")
    if args.filter_by not in ["gene_name", "gene_id", "transcript_id"]:
        print("! Select a proper filter type :\n\tgene_name, gene_id or transcript_id")
    filter_by = args.filter_by
    search_by = args.search_by
    dataset = args.dataset

# gnomAD Parameters and API Function
end_point = "https://gnomad.broadinstitute.org/api/"

def get_variants_by(filter_by, search_term, dataset, timeout=None):
    query = """
    {
      %s(%s: "%s") {
        variants(dataset: %s) {
          gene_id
          gene_symbol
          chrom
          pos
          rsid
          ref
          alt
          consequence
          genome {
            genome_af:af
            genome_ac:ac
            genome_an:an
            genome_ac_hemi:ac_hemi
            genome_ac_hom:ac_hom
          }
          exome {
            exome_af:af
            exome_ac:ac
            exome_an:an
            exome_ac_hemi:ac_hemi
            exome_ac_hom:ac_hom
          }
          flags
          lof
          consequence_in_canonical_transcript
          gene_symbol
          hgvsc
          lof_filter
          lof_flags
          hgvsc
          hgvsp
          reference_genome
          variant_id: variantId
        }
      }
    }
    """
    if filter_by == "transcript_id":
        query = query % ("transcript", filter_by, search_term, dataset)
    else:
        query = query % ("gene", filter_by, search_term, dataset)
    response = requests.post(end_point, data={'query': query}, timeout=timeout)
    if response.status_code == 200:
        try:
            if filter_by == "transcript_id":
                data = json_normalize(response.json()["data"]["transcript"]["variants"])
            else:
                data = json_normalize(response.json()["data"]["gene"]["variants"])
            data.columns = data.columns.map(lambda x: x.split(".")[-1])
            data.to_csv("outputs/" + search_term + ".tsv", sep="\t", index=False) 
            # return data
        except (KeyError, TypeError):
            print(str(response["error"]))
        except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
            print("An unknown error occured regarding the internet connection!")
    elif response.status_code == 404:
        print('API is not accessible right now. Check the end point out!')

# Action
if __name__ == "__main__":
    arg_parser()
    if "." in search_by.upper():
        try:
            with open(search_by, "r") as f:
                gene_list = [line.rstrip() for line in f]
                for tmp_gene in tqdm(gene_list):
                    get_variants_by(filter_by, tmp_gene.upper(), dataset)
        except:
            print("A problem occured while reading the file namely {} or the type {} you selected is wrong!"\
                  .format(search_by, filter_by))
        finally:
            f.close()
    elif "." not in search_by.upper():
        get_variants_by(filter_by, search_by.upper(), dataset)
