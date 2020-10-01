# gnomAD Python API by @furkanmtorun 
# E-Mail:               furkanmtorun@gmail.com 
# GitHub:               https://github.com/furkanmtorun  
# Google Scholar:       https://scholar.google.com/citations?user=d5ZyOZ4AAAAJ
# Personal Website :    https://furkanmtorun.github.io/

# Import required libraries and packages
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from pandas.io.json import json_normalize as json_normalize
import plotly.express as px
import streamlit as st
import pandas as pd
import requests
import json
import os
import shutil

# Create folders for outputs in the current directory
if not os.path.exists('outputs/'):
    os.mkdir('outputs/')

# gnomAD API
end_point = "https://gnomad.broadinstitute.org/api/"

# Welcome
main_external_css = """
    <style>
        #MainMenu, .reportview-container .main footer {display: none;}
    </style>
"""
version = "v1.0"
citation = "TORUN FM., (2020) gnomAD Python API. "

st.markdown(main_external_css, unsafe_allow_html=True)
st.title("🧬 gnomAD Python API {}".format(version))

st.markdown("""
        
        > #### 📰 Developer and Citation
        > - gnomAD Python API {} by **Furkan M. Torun**
        > - E-Mail:               [furkanmtorun@gmail.com](mailto:furkanmtorun@gmail.com) 
        > - GitHub:               https://github.com/furkanmtorun  
        > - Google Scholar:       https://scholar.google.com/citations?user=d5ZyOZ4AAAAJ
        > - Personal Website :    https://furkanmtorun.github.io/
        > - Cite as follows:
        >
        >    `{}`
        
        ---
    """.format(version, citation))

st.info(""" 
        - This API tool uses [gnomAD GraphQL backend service](https://gnomad.broadinstitute.org/api).
        - Upload your .csv/tsv/txt file containing the single type of identifiers as one column.
        - Each row should correspond to single record (i.e. gene name, gene ID, rsID, transcript ID).
        - By using the app, you agree that you accepting [the disclaimer](https://github.com/furkanmtorun/gnomad_python_api#hash-disclaimer).
    """)

# File - content uploading
@st.cache(persist=True)
def upload_file(file_buffer):
    df = pd.DataFrame()
    if file_buffer is not None:
        try:
            df = pd.read_csv(file_buffer, sep=",", header=None, names=["search_term"])
        except:
            df = pd.read_csv(file_buffer, sep='\t', header=None, names=["search_term"])
    return df

# Input
st.subheader("Set the input")
file_buffer = st.file_uploader("Upload your search list below as *.csv, *.tsv or *.txt (without header):", type=["csv", "tsv", "txt"])

if file_buffer is not None:
    search_df = upload_file(file_buffer)
    search_by = search_df
    st.text("Here is your file:")
    st.dataframe(search_df)
if file_buffer is None:
    single_search = st.text_input("Or write a single ID here:", value="TP53")
    search_by = single_search

# Input type
st.subheader("Select the input type")
filter_by = st.selectbox("Select a proper input type", ["gene_name", "gene_id", "transcript_id", "rs_id"])

# Datasets
st.subheader("Choose the source for dataset")
dataset = st.selectbox("Select a proper gnomAD data set:", ["gnomad_r2_1", "gnomad_r3", "gnomad_r2_1_controls", "gnomad_r2_1_non_neuro", "gnomad_r2_1_non_cancer", "gnomad_r2_1_non_topmed", "exac"])

# SV Dataset
if filter_by in ["gene_id", "gene_name"]:
    st.subheader("Choose the source for structural variant (SV) dataset")
    sv_dataset = st.selectbox("Select a proper SV gnomAD data set:", ["gnomad_sv_r2_1", "gnomad_sv_r2_1_controls", "gnomad_sv_r2_1_non_neuro"])

# Main Function for Getting Data and Saving them
def get_variants_by(filter_by, search_term, dataset, mode, timeout=None):

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
    global response
    response = requests.post(end_point, data={'query': query}, timeout=timeout)
    
    # Parse response
    if response.status_code == 200:

        st.markdown("---")
        st.subheader("Outputs for `{}`  is being prepared.".format(search_term))
        st.markdown("\n")
        
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
                    if (len(data) > 0) and (mode == "single"):
                        st.markdown("\n **Table for: `" + json_key + "`**")
                        st.dataframe(data)

        elif filter_by == "rs_id":
            if not os.path.exists('outputs/' + search_term + "/"):
                os.mkdir('outputs/'+ search_term + "/")
            else:
                shutil.rmtree('outputs/'+ search_term + "/")
                os.mkdir('outputs/'+ search_term + "/")
            json_keys = list(response.json()["data"]["variant"].keys())

            general_info = "```"
            for json_key in json_keys:
                # print(json_key, type(response.json()["data"]["variant"][json_key]))

                # Basic info in `variant` part
                if response.json()["data"]["variant"][json_key] is not None and type(response.json()["data"]["variant"][json_key]) in [str, int]:
                    with open("outputs/" + search_term + "/" + search_term + ".txt", "a") as f:
                        f.write("\n" + json_key + ":" + str(response.json()["data"]["variant"][json_key]))
                        general_info += "\n" + json_key + ":" + str(response.json()["data"]["variant"][json_key])
                # Other parts rather than `genome` and `exome`
                if response.json()["data"]["variant"][json_key] is not None and type(response.json()["data"]["variant"][json_key]) not in [str, int] and json_key not in ["genome", "exome"]:
                    data = json_normalize(response.json()["data"]["variant"][json_key])
                    data.columns = data.columns.map(lambda x: x.split(".")[-1])
                    data.to_csv("outputs/" + search_term + "/" + json_key + ".tsv", sep="\t", index=False)
                    if (len(data) > 0) and (mode == "single"):
                        st.markdown("\n **Table for: `" + json_key + "`**")
                        st.dataframe(data)

                # Deep parsing for nested things in `genome` and `exome`
                if json_key in ["genome", "exome"]:
                    for sub_json_key in list(response.json()["data"]["variant"][json_key].keys()):
                        # print(json_key, sub_json_key, type(response.json()["data"]["variant"][json_key][sub_json_key]))
                        
                        if response.json()["data"]["variant"][json_key][sub_json_key] is not None and type(response.json()["data"]["variant"][json_key][sub_json_key]) in [str, int]:
                            with open("outputs/" + search_term + "/" + search_term + ".txt", "a") as f:
                                f.write("\n" + json_key + "_" + sub_json_key + ":" + str(response.json()["data"]["variant"][json_key][sub_json_key]))
                                general_info += "\n" + json_key + "_" + sub_json_key + ":" + str(response.json()["data"]["variant"][json_key][sub_json_key])

                        if response.json()["data"]["variant"][json_key][sub_json_key] is not None and type(response.json()["data"]["variant"][json_key][sub_json_key]) not in [str, int]:
                            data = json_normalize(response.json()["data"]["variant"][json_key][sub_json_key])
                            data.columns = data.columns.map(lambda x: x.split(".")[-1])
                            data.to_csv("outputs/" + search_term + "/" + json_key + "_" + sub_json_key + ".tsv", sep="\t", index=False)    
                            if (len(data) > 0) and (mode == "single"):
                                st.markdown("\n **Table for: `" + sub_json_key + "`**")
                                st.dataframe(data) 

            general_info += "```"
            if mode == "single":
                st.markdown("--- \n **General Info for your query**")
                st.info(general_info)

        elif filter_by == "gene_id":
            if not os.path.exists('outputs/' + search_term + "/"):
                os.mkdir('outputs/'+ search_term + "/")
            else:
                shutil.rmtree('outputs/'+ search_term + "/")
                os.mkdir('outputs/'+ search_term + "/")

            json_keys = list(response.json()["data"]["gene"].keys())
            general_info ="```"
            for json_key in json_keys:
                # print(json_key, type(response.json()["data"]["gene"][json_key]), response.json()["data"]["gene"][json_key] is None, type(response.json()["data"]["gene"][json_key]) not in [str, int])
                if response.json()["data"]["gene"][json_key] is not None and type(response.json()["data"]["gene"][json_key]) in [str, int]:
                    with open("outputs/" + search_term + "/" + search_term + ".txt", "a") as f:
                        f.write("\n" + json_key + ":" + str(response.json()["data"]["gene"][json_key]))
                        general_info += "\n" + json_key + ":" + str(response.json()["data"]["gene"][json_key])

                if response.json()["data"]["gene"][json_key] is not None and type(response.json()["data"]["gene"][json_key]) not in [str, int]:
                    data = json_normalize(response.json()["data"]["gene"][json_key])
                    data.columns = data.columns.map(lambda x: x.split(".")[-1])
                    data.to_csv("outputs/" + search_term + "/" + json_key + ".tsv", sep="\t", index=False)
                    if (len(data) > 0) and (mode == "single"):
                        st.markdown("\n **Table for: `" + json_key + "`**")
                        st.dataframe(data)
            
            general_info += "```"
            if mode == "single":
                st.markdown("--- \n **General Info for your query**")
                st.info(general_info)

        elif filter_by == "gene_name":
            if not os.path.exists('outputs/' + search_term + "/"):
                os.mkdir('outputs/'+ search_term + "/")
            else:
                shutil.rmtree('outputs/'+ search_term + "/")
                os.mkdir('outputs/'+ search_term + "/")

            json_keys = list(response.json()["data"]["gene"].keys())
            general_info ="```"
            for json_key in json_keys:
                # print(json_key, type(response.json()["data"]["gene"][json_key]), response.json()["data"]["gene"][json_key] is None, type(response.json()["data"]["gene"][json_key]) not in [str, int])
                if response.json()["data"]["gene"][json_key] is not None and type(response.json()["data"]["gene"][json_key]) in [str, int]:
                    with open("outputs/" + search_term + "/" + search_term + ".txt", "a") as f:
                        f.write("\n" + json_key + ": " + str(response.json()["data"]["gene"][json_key]))
                    general_info += ("\n" + json_key + ": " + str(response.json()["data"]["gene"][json_key]))
            
                if response.json()["data"]["gene"][json_key] is not None and type(response.json()["data"]["gene"][json_key]) not in [str, int]:
                    data = json_normalize(response.json()["data"]["gene"][json_key])
                    data.columns = data.columns.map(lambda x: x.split(".")[-1])
                    data.to_csv("outputs/" + search_term + "/" + json_key + ".tsv", sep="\t", index=False)
                    if (len(data) > 0) and (mode == "single"):
                        st.markdown("\n **Table for: `" + json_key + "`**")
                        st.dataframe(data)

            general_info += "```"
            if mode == "single":
                st.markdown("--- \n **General Info for your query**")
                st.info(general_info)
        
    return response

# Plotting
## Generate grouping and freq plot
def make_grouping_freq_plot(df, group_by, title):
    df[group_by] = df[group_by].str.replace("_", " ").str.title()
    df2 = df.groupby(group_by).size().reset_index(name='Number of Variants')
    fig = px.bar(df2, x=group_by, y="Number of Variants", color=group_by, barmode='stack', template="ggplot2",
                hover_data=[group_by]).for_each_trace(lambda t: t.update(name=t.name.split("=")[1]))
    fig.update_layout(
                    title_text=title,
                    xaxis_tickangle=-45,
                    yaxis=dict(title='Variants', titlefont_size=14, tickfont_size=12),
                    xaxis=dict(
                        title="Categories of {}".format(group_by.replace("_", " ").title()), 
                        titlefont_size=14, 
                        tickfont_size=12))
    return fig

def generate_plot(search_by, filter_by, mode):
    st.subheader("Plots \n ")
    try:
        if filter_by in ["gene_name", "gene_id", "transcript_id"]:
            variant_file = "./outputs/" + search_by + "/variants.tsv"

            if os.path.isfile(variant_file):
                ## gnomad
                variants_df = pd.read_csv(variant_file, sep="\t")
                fig1 = make_grouping_freq_plot(variants_df, "consequence", 'Consequence of gnomAD Variants')
                fig2 = make_grouping_freq_plot(variants_df, "lof", 'LoF of gnomAD Variants')
                fig3 = make_grouping_freq_plot(variants_df, "lof_filter", 'LoF Filtes of gnomAD Variants')
                
                ## clinvar
                clivar_df = pd.read_csv("./outputs/" + search_by + "/clinvar_variants.tsv", sep="\t")
                clivar_df["clinical_significance"] = clivar_df["clinical_significance"].apply(lambda x: x.split("'")[1])
                fig4 = make_grouping_freq_plot(clivar_df, "clinical_significance", 'Clinical Significance of ClinVar Variants')
                fig5 = make_grouping_freq_plot(clivar_df, "major_consequence", 'Major Consequence of ClinVar Variants')
                
                # Show in the app
                if mode == "single":
                    st.plotly_chart(fig1)
                    st.plotly_chart(fig2)
                    st.plotly_chart(fig3)
                    st.plotly_chart(fig4)
                    st.plotly_chart(fig5)
                
                # Export as HTML
                fig1.write_html("./outputs/" + search_by + "/gnomAD_variants_by_consequence.html")
                fig2.write_html("./outputs/" + search_by + "/gnomAD_variants_by_lof.html")
                fig3.write_html("./outputs/" + search_by + "/gnomAD_variants_by_lof_filter.html")
                fig4.write_html("./outputs/" + search_by + "/clinvar_variants_by_clinical_significance.html")
                fig5.write_html("./outputs/" + search_by + "/clinvar_variants_by_major_consequence.html")
            else:
                st.warning("Plots were not generated since `variants.tsv` could be created. It may happens if the data is not available for your dataset")

        if filter_by in ["gene_name", "gene_id"]:
            structural_variants_file = "./outputs/" + search_by + "/structural_variants.tsv"
            if os.path.isfile(variant_file):
                ## structural_variants
                sv_df = pd.read_csv(structural_variants_file, sep="\t")
                fig6 = make_grouping_freq_plot(sv_df, "consequence", 'Major Consequence of Structural Variants')
                
                # Show in the app
                if mode == "single":
                    st.plotly_chart(fig6)

                # Export as HTML
                fig6.write_html("./outputs/" + search_by + "/structural_variants_by_consequence.html")
            else:
                st.warning("Plots were not generated since `structural_variants.tsv` could be created. It may happens if the data is not available for your dataset")

    except Exception as plotError:
        st.text(plotError)
        pass

# Action
if (filter_by is not None) and (search_by is not None) and (st.button('Get Data and Generate Plots', key='run')):
    try:
        if file_buffer is None:
            # Single
                with st.spinner('Getting data and generating the plots ...'):
                    response = get_variants_by(filter_by, search_by, dataset, "single")
                    if response.status_code in [404, 405, 503]:
                        st.error('API is not accessible right now. Check the end point out for gnomAD API!')
                        st.markdown("""
                                > For techinal detail, status code is `{}` and
                                > 
                                > current end point is `{}`.
                            """.format(response.status_code, end_point))
                    
                    else:
                        generate_plot(search_by, filter_by, "single")
                        st.markdown("\n --- \n")
                        st.success("DONE! Check your `outputs/` folder.")
                    
        elif file_buffer is not None:
            # Multiple
            with st.spinner('Getting data and will back soon...'):
                for i, search_item in search_df.iterrows():
                    response = get_variants_by(filter_by, search_item[0], dataset, "multiple")
                    
                    if response.status_code in [404, 405, 503]:
                        st.error('API is not accessible right now. Check the end point out for gnomAD API!')
                        st.markdown("""
                                > For techinal detail, status code is `{}` and
                                > 
                                > current end point is `{}`.
                            """.format(response.status_code, end_point))
                    
                    else:
                        generate_plot(search_item[0], filter_by, "multiple")
                        st.progress(100)
                        
                st.markdown("\n --- \n")
                st.success("DONE! Check your `outputs/` folder.")

    except (ConnectionError, ConnectionAbortedError, ConnectionRefusedError, ConnectionResetError):
        st.error("An unknown error occured regarding the internet connection!")
        
    except AttributeError as ae:

        # Error Message from gnomAD 
        if filter_by != 'rs_id':
            try:
                for msg in response.json()["errors"]:
                    st.error("Errors from gnomAD for your process:\n\t" + msg["message"])
            except Exception as anyOtherException:
                pass
    
            # General Error Message
            st.warning("""
                It might be caused since the search did not find a result from the database. 
                Try to check the `input` for `{}` or other `options`.
                """.format(filter_by))
            
            # Technical Error Message 
            st.markdown("""
                > As a note, technical reason is `{}`. 
                > 
                > If you think this should not occur, you can contact with developer to issue this problem on Github page.
                """.format(ae))
        else:
            pass

    except (TypeError, KeyError):
        try:
            for msg in response.json()["errors"]:
                st.error("Errors from gnomAD for your process:\n\t" + msg["message"])
        except Exception as anyOtherException:
            pass