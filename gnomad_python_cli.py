# gnomAD Python API by @furkanmtorun 
# E-Mail:               furkanmtorun@gmail.com 
# GitHub:               https://github.com/furkanmtorun  
# Google Scholar:       https://scholar.google.com/citations?user=d5ZyOZ4AAAAJ
# Personal Website :    https://furkanmtorun.github.io/

# Import required libraries and packages
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from pandas.io.json import json_normalize as json_normalize
from tqdm import tqdm
import pandas as pd
import requests
import argparse
import json
import os
import shutil
import sys

# Create folders for outputs in the current directory
if not os.path.exists('outputs/'):
    os.mkdir('outputs/')

# Argument Parsing
def arg_parser():
    global filter_by
    global search_by
    global dataset
    global sv_dataset
    parser = argparse.ArgumentParser()
    parser.add_argument("-filter_by", type=str, required=True, default="gene_name", help="Get your variants according to: `gene_name`, `gene_id, `transcript_id` or `rs_id`.")
    parser.add_argument("-search_by", type=str, required=True, default="TP53", help="Type your input for searching or type the file name (e.g: myGenes.txt) containing your inputs")
    parser.add_argument("-dataset", type=str, required=True, default="gnomad_r2_1", help="Select your dataset: exac, gnomad_r2_1, gnomad_r3, gnomad_r2_1_controls, gnomad_r2_1_non_neuro, gnomad_r2_1_non_cancer, gnomad_r2_1_non_topmed")
    parser.add_argument("-sv_dataset", type=str, required=False, default="gnomad_sv_r2_1", help="Select your structural variants dataset : `gnomad_sv_r2_1`, `gnomad_sv_r2_1_controls` or `gnomad_sv_r2_1_non_neuro`")
    # parser.add_argument("-get", nargs="+", default=["gnomad", "clinvar"], help="List your requests comma seperated: `gnomad`, `clinvar`, `gtex_tissue_expression`, `genome_coverage`, `exome_coverage`, `gnomad_constraint`, or `exac_constraint`")
    args = parser.parse_args()
    
    # Control the given arguments 
    if args.dataset not in ["exac", "gnomad_r2_1", "gnomad_r3", "gnomad_r2_1_controls", "gnomad_r2_1_non_neuro", "gnomad_r2_1_non_cancer", "gnomad_r2_1_non_topmed"]:
        sys.exit("! Select a proper gnomAD data set:\n\texac, gnomad_r2_1, gnomad_r3, gnomad_r2_1_controls, gnomad_r2_1_non_neuro, gnomad_r2_1_non_cancer, gnomad_r2_1_non_topmed")

    if args.sv_dataset not in ["gnomad_sv_r2_1", "gnomad_sv_r2_1_controls", "gnomad_sv_r2_1_non_neuro"]:
        sys.exit("! Select a proper gnomAD data set:\n\t`gnomad_sv_r2_1`, `gnomad_sv_r2_1_controls` or `gnomad_sv_r2_1_non_neuro`")
    
    if args.filter_by not in ["gene_name", "gene_id", "transcript_id", "rs_id"]:
        sys.exit("! Select a proper filter type :\n\t `gene_name`, `gene_id, `transcript_id` or `rs_id`")

    # Define variables
    filter_by = args.filter_by
    search_by = args.search_by
    dataset = args.dataset
    sv_dataset = args.sv_dataset

    return filter_by, search_by, dataset, sv_dataset

# gnomAD API
end_point = "https://gnomad.broadinstitute.org/api/"

# Main Function
def get_variants_by(filter_by, search_term, dataset, timeout=None):
    
    query_for_transcripts = """
    {
        transcript(transcript_id: "%s") {
            transcript_id,
            transcript_version,        
            gene {
            gene_id,
            symbol,
            start,
            stop,
            strand,
            chrom,
            hgnc_id,
            gene_name,
            full_gene_name,
            omim_id
            }
            variants(dataset: %s) {
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
            gtex_tissue_expression{
            adipose_subcutaneous,
            adipose_visceral_omentum,
            adrenal_gland,
            artery_aorta,
            artery_coronary,
            artery_tibial,
            bladder,
            brain_amygdala,
            brain_anterior_cingulate_cortex_ba24,
            brain_caudate_basal_ganglia,
            brain_cerebellar_hemisphere,
            brain_cerebellum,
            brain_cortex,
            brain_frontal_cortex_ba9,
            brain_hippocampus,
            brain_hypothalamus,
            brain_nucleus_accumbens_basal_ganglia,
            brain_putamen_basal_ganglia,
            brain_spinal_cord_cervical_c_1,
            brain_substantia_nigra,
            breast_mammary_tissue,
            cells_ebv_transformed_lymphocytes,
            cells_transformed_fibroblasts,
            cervix_ectocervix,
            cervix_endocervix,
            colon_sigmoid,
            colon_transverse,
            esophagus_gastroesophageal_junction,
            esophagus_mucosa,
            esophagus_muscularis,
            fallopian_tube,
            heart_atrial_appendage,
            heart_left_ventricle,
            kidney_cortex,
            liver,
            lung,
            minor_salivary_gland,
            muscle_skeletal,
            nerve_tibial,
            ovary,
            pancreas,
            pituitary,
            prostate,
            skin_not_sun_exposed_suprapubic,
            skin_sun_exposed_lower_leg,
            small_intestine_terminal_ileum,
            spleen,
            stomach,
            testis,
            thyroid,
            uterus,
            vagina,
            whole_blood
            }
            clinvar_variants{
                variant_id,
                clinvar_variation_id,
                reference_genome,
                chrom,
                pos,
                ref,
                alt,
                clinical_significance,
                gold_stars,
                major_consequence,
                review_status
            }
            coverage(dataset: %s){
              genome{
                pos,
                mean,
                median,
                over_1,
                over_5,
                over_10,
                over_15,
                over_20,
                over_25,
                over_30,
                over_50,
                over_100
              }

              exome{
                pos,
                mean,
                median,
                over_1,
                over_5,
                over_10,
                over_15,
                over_20,
                over_25,
                over_30,
                over_50,
                over_100
              }
            }
            gnomad_constraint{
            exp_lof,
            exp_mis,
            exp_syn,
            obs_lof,
            obs_mis,
            obs_syn,
            oe_lof,
            oe_lof_lower,
            oe_lof_upper,
            oe_mis,
            oe_mis_lower,
            oe_mis_upper,
            oe_syn,
            oe_syn_lower,
            oe_syn_upper,
            lof_z,
            mis_z,
            syn_z,
            pLI,
            flags
            }
            exac_constraint{
            exp_syn,
            exp_mis,
            exp_lof,
            obs_syn,
            obs_mis,
            obs_lof,
            mu_syn,
            mu_mis,
            mu_lof,
            syn_z,
            mis_z,
            lof_z,
            pLI
            }
        }
    }
    """

    query_for_variants = """
    {
        variant(%s: "%s", dataset: %s) {
        variantId
        reference_genome
        chrom
        pos
        ref
        alt
        colocatedVariants
        multiNucleotideVariants {
        combined_variant_id
        changes_amino_acids
        n_individuals
        other_constituent_snvs
        }
        exome {
        ac
        an
        ac_hemi
        ac_hom
        faf95 {
            popmax
            popmax_population
        }
        filters
        populations {
            id
            ac
            an
            ac_hemi
            ac_hom
        }
        age_distribution {
            het {
            bin_edges
            bin_freq
            n_smaller
            n_larger
            }
            hom {
            bin_edges
            bin_freq
            n_smaller
            n_larger
            }
        }
        qualityMetrics {
            alleleBalance {
            alt {
                bin_edges
                bin_freq
                n_smaller
                n_larger
            }
            }
            genotypeDepth {
            all {
                bin_edges
                bin_freq
                n_smaller
                n_larger
            }
            alt {
                bin_edges
                bin_freq
                n_smaller
                n_larger
            }
            }
            genotypeQuality {
            all {
                bin_edges
                bin_freq
                n_smaller
                n_larger
            }
            alt {
                bin_edges
                bin_freq
                n_smaller
                n_larger
            }
            }
            siteQualityMetrics {
            BaseQRankSum
            ClippingRankSum
            DP
            FS
            InbreedingCoeff
            MQ
            MQRankSum
            pab_max
            QD
            ReadPosRankSum
            RF
            SiteQuality
            SOR
            VQSLOD
            }
        }
        }
        genome {
        ac
        an
        ac_hemi
        ac_hom
        faf95 {
            popmax
            popmax_population
        }
        filters
        populations {
            id
            ac
            an
            ac_hemi
            ac_hom
        }
        age_distribution {
            het {
            bin_edges
            bin_freq
            n_smaller
            n_larger
            }
            hom {
            bin_edges
            bin_freq
            n_smaller
            n_larger
            }
        }
        qualityMetrics {
            alleleBalance {
            alt {
                bin_edges
                bin_freq
                n_smaller
                n_larger
            }
            }
            genotypeDepth {
            all {
                bin_edges
                bin_freq
                n_smaller
                n_larger
            }
            alt {
                bin_edges
                bin_freq
                n_smaller
                n_larger
            }
            }
            genotypeQuality {
            all {
                bin_edges
                bin_freq
                n_smaller
                n_larger
            }
            alt {
                bin_edges
                bin_freq
                n_smaller
                n_larger
            }
            }
            siteQualityMetrics {
            BaseQRankSum
            ClippingRankSum
            DP
            FS
            InbreedingCoeff
            MQ
            MQRankSum
            pab_max
            QD
            ReadPosRankSum
            RF
            SiteQuality
            SOR
            VQSLOD
            }
        }
        }
        flags
        rsid
        sortedTranscriptConsequences {
        canonical
        gene_id
        gene_version
        gene_symbol
        hgvs
        hgvsc
        hgvsp
        lof
        lof_flags
        lof_filter
        major_consequence
        polyphen_prediction
        sift_prediction
        transcript_id
        transcript_version
        }
        }
    
    }
    """

    query_for_genes = """
    {
        gene(%s: "%s") {
                gene_id
            symbol
            start
            stop
            strand
            chrom
            hgnc_id
            gene_name
                symbol
            full_gene_name
                reference_genome
            omim_id
                canonical_transcript_id
            
            structural_variants(dataset: %s){
            ac,
            ac_hom,
            an,
            af,
            reference_genome,
            chrom,
            chrom2,
            end,
            end2,
            consequence,
            filters,
            length,
            pos,
            pos2,
            type,
            variant_id
            }
            
            variants(dataset: %s) {
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
                
            mane_select_transcript{
            ensembl_id
            ensembl_version
            refseq_id
            refseq_version
            }
            
            transcripts{
            reference_genome
            gene_id
            transcript_id
            strand
            start
            stop
            chrom
            }
            
            exac_regional_missense_constraint_regions {
            start
            stop
            obs_mis
            exp_mis
            obs_exp
            chisq_diff_null
            }
            
            clinvar_variants {
            variant_id
            clinvar_variation_id
            reference_genome
            chrom
            pos
            ref
            alt
            clinical_significance
            gold_stars
            major_consequence
            review_status
            }
            
            coverage(dataset: %s) {
                exome {
                pos
                mean
                median
                over_1
                over_5
                over_10
                over_15
                over_20
                over_25
                over_30
                over_50
                over_100
                }
                genome {
                pos
                mean
                median
                over_1
                over_5
                over_10
                over_15
                over_20
                over_25
                over_30
                over_50
                over_100
                }
            }
            
            
            gnomad_constraint {
            exp_lof
            exp_mis
            exp_syn
            obs_lof
            obs_mis
            obs_syn
            oe_lof
            oe_lof_lower
            oe_lof_upper
            oe_mis
            oe_mis_lower
            oe_mis_upper
            oe_syn
            oe_syn_lower
            oe_syn_upper
            lof_z
            mis_z
            syn_z
            pLI
            flags
            }
            
            exac_constraint {
            exp_syn
            exp_mis
            exp_lof
            obs_syn
            obs_mis
            obs_lof
            mu_syn
            mu_mis
            mu_lof
            syn_z
            mis_z
            lof_z
            pLI
            }
        }
    }
    """

    if filter_by == "transcript_id":
        query = query_for_transcripts % (search_term.upper(), dataset, dataset)

    elif filter_by == "rs_id":
        query = query_for_variants % ("rsid", search_term.lower(), dataset)

    elif filter_by == "gene_id":
        query = query_for_genes % ("gene_id", search_term.upper(), sv_dataset, dataset, dataset)
    
    elif filter_by == "gene_name":
        query = query_for_genes % ("gene_name", search_term.upper(), sv_dataset, dataset, dataset)

    else:
        print("Unknown `filter_by` type!")

    # Get repsonse
    response = requests.post(end_point, data={'query': query}, timeout=timeout)
    
    # Parse response
    if response.status_code == 200:
        try:

            if filter_by == "transcript_id":
                if not os.path.exists('outputs/' + search_term + "/"):
                    os.mkdir('outputs/'+ search_term + "/")
                else:
                    shutil.rmtree('outputs/'+ search_term + "/")
                    os.mkdir('outputs/'+ search_term + "/")
                json_keys = list(response.json()["data"]["transcript"].keys())
                for json_key in json_keys:
                    if response.json()["data"]["transcript"][json_key] is not None and type(response.json()["data"]["transcript"][json_key]) not in [str, int]:
                        data = json_normalize(response.json()["data"]["transcript"][json_key])
                        data.columns = data.columns.map(lambda x: x.split(".")[-1])
                        data.to_csv("outputs/" + search_term + "/" + json_key + ".tsv", sep="\t", index=False) 

            elif filter_by == "rs_id":
                if not os.path.exists('outputs/' + search_term + "/"):
                    os.mkdir('outputs/'+ search_term + "/")
                else:
                    shutil.rmtree('outputs/'+ search_term + "/")
                    os.mkdir('outputs/'+ search_term + "/")
                json_keys = list(response.json()["data"]["variant"].keys())
                for json_key in json_keys:
                    # print(json_key, type(response.json()["data"]["variant"][json_key]))

                    # Basic info in `variant` part
                    if response.json()["data"]["variant"][json_key] is not None and type(response.json()["data"]["variant"][json_key]) in [str, int]:
                        with open("outputs/" + search_term + "/" + search_term + ".txt", "a") as f:
                            f.write("\n" + json_key + ":" + str(response.json()["data"]["variant"][json_key]))
                    
                    # Other parts rather than `genome` and `exome`
                    if response.json()["data"]["variant"][json_key] is not None and type(response.json()["data"]["variant"][json_key]) not in [str, int] and json_key not in ["genome", "exome"]:
                        data = json_normalize(response.json()["data"]["variant"][json_key])
                        data.columns = data.columns.map(lambda x: x.split(".")[-1])
                        data.to_csv("outputs/" + search_term + "/" + json_key + ".tsv", sep="\t", index=False)

                    # Deep parsing for nested things in `genome` and `exome`
                    if json_key in ["genome", "exome"]:
                        for sub_json_key in list(response.json()["data"]["variant"][json_key].keys()):
                            # print(json_key, sub_json_key, type(response.json()["data"]["variant"][json_key][sub_json_key]))
                            
                            if response.json()["data"]["variant"][json_key][sub_json_key] is not None and type(response.json()["data"]["variant"][json_key][sub_json_key]) in [str, int]:
                                with open("outputs/" + search_term + "/" + search_term + ".txt", "a") as f:
                                    f.write("\n" + json_key + "_" + sub_json_key + ":" + str(response.json()["data"]["variant"][json_key][sub_json_key]))

                            if response.json()["data"]["variant"][json_key][sub_json_key] is not None and type(response.json()["data"]["variant"][json_key][sub_json_key]) not in [str, int]:
                                data = json_normalize(response.json()["data"]["variant"][json_key][sub_json_key])
                                data.columns = data.columns.map(lambda x: x.split(".")[-1])
                                data.to_csv("outputs/" + search_term + "/" + json_key + "_" + sub_json_key + ".tsv", sep="\t", index=False)     

            elif filter_by == "gene_id":
                if not os.path.exists('outputs/' + search_term + "/"):
                    os.mkdir('outputs/'+ search_term + "/")
                else:
                    shutil.rmtree('outputs/'+ search_term + "/")
                    os.mkdir('outputs/'+ search_term + "/")

                json_keys = list(response.json()["data"]["gene"].keys())
                for json_key in json_keys:
                    # print(json_key, type(response.json()["data"]["gene"][json_key]), response.json()["data"]["gene"][json_key] is None, type(response.json()["data"]["gene"][json_key]) not in [str, int])
                    if response.json()["data"]["gene"][json_key] is not None and type(response.json()["data"]["gene"][json_key]) in [str, int]:
                        with open("outputs/" + search_term + "/" + search_term + ".txt", "a") as f:
                            f.write("\n" + json_key + ":" + str(response.json()["data"]["gene"][json_key]))

                    if response.json()["data"]["gene"][json_key] is not None and type(response.json()["data"]["gene"][json_key]) not in [str, int]:
                        data = json_normalize(response.json()["data"]["gene"][json_key])
                        data.columns = data.columns.map(lambda x: x.split(".")[-1])
                        data.to_csv("outputs/" + search_term + "/" + json_key + ".tsv", sep="\t", index=False)

            elif filter_by == "gene_name":
                if not os.path.exists('outputs/' + search_term + "/"):
                    os.mkdir('outputs/'+ search_term + "/")
                else:
                    shutil.rmtree('outputs/'+ search_term + "/")
                    os.mkdir('outputs/'+ search_term + "/")

                json_keys = list(response.json()["data"]["gene"].keys())
                for json_key in json_keys:
                    # print(json_key, type(response.json()["data"]["gene"][json_key]), response.json()["data"]["gene"][json_key] is None, type(response.json()["data"]["gene"][json_key]) not in [str, int])
                    if response.json()["data"]["gene"][json_key] is not None and type(response.json()["data"]["gene"][json_key]) in [str, int]:
                        with open("outputs/" + search_term + "/" + search_term + ".txt", "a") as f:
                            f.write("\n" + json_key + ":" + str(response.json()["data"]["gene"][json_key]))

                    if response.json()["data"]["gene"][json_key] is not None and type(response.json()["data"]["gene"][json_key]) not in [str, int]:
                        data = json_normalize(response.json()["data"]["gene"][json_key])
                        data.columns = data.columns.map(lambda x: x.split(".")[-1])
                        data.to_csv("outputs/" + search_term + "/" + json_key + ".tsv", sep="\t", index=False)
                
        except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
            sys.exit("An unknown error occured regarding the internet connection!")
        
        except AttributeError as ae:
            pass

        except (TypeError, KeyError):
            for msg in response.json()["errors"]:
                sys.exit("Errors from gnomAD for your process:\n\t" + msg["message"])

        else:
            print(" ! DONE: Check out the 'outputs/' folder")

    elif response.status_code == 404:
        sys.exit('API is not accessible right now. Check the end point out!')

# Action
if __name__ == "__main__":
    filter_by, search_by, dataset, sv_dataset = arg_parser()
    if "." in search_by:
        try:
            with open(search_by, "r") as f:
                search_list = [line.rstrip() for line in f]
                for search_item in tqdm(search_list):
                    get_variants_by(filter_by, search_item, dataset)
        except:
            print("A problem occured while reading the file namely `{}` or the filter type `{}` is wrong!"\
                  .format(search_by, filter_by))
        finally:
            f.close()
    elif "." not in search_by:
        get_variants_by(filter_by, search_by, dataset)
        