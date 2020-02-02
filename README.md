# 🧬 gnomAD Python API (Batch Script)

## :hash: What is *gnomAD* and the purpose of this script?
[gnomAD (The Genome Aggregation Database)](http://gnomad.broadinstitute.org/) is aggregation of thousands of exomes and genomes human sequencing studies. Also, gnomAD consortium annotates the variants with allelic frequency in genomes and exomes.
**Here**, this batch script is able to search the genes or transcripts of your interest and retrieve variant data from the database via [gnomAD backend API](https://gnomad.broadinstitute.org/api) that based on GraphQL query language.

## :hash: Requirements and Installation
 - Create a directory and download the "**gnomad_python_api.py**" and "**requirements.txt**" files or clone the repository via Git using following command:
 
 	`git clone https://github.com/furkanmtorun/gnomad_python_api.git`

 - Install the required packages if you do not already:
 
	` pip3 install -r requirements.txt `

- It's ready to use now! 

> If you did not install **pip** yet, please follow the instruction [here](https://pip.pypa.io/en/stable/installing/).

## :hash: Usage & Options
| Options in the script | Description | Parameters |
|--|--|--|
| -filter_by | *It defines the input type* |gene_name, gene_id, transcript_id |
| -search_by | *It defines the input* | Type a gene/transcript identifier <br> *e.g.: TP53, ENSG00000169174, ENST00000544455* <br> Type the name of file containig your inputs <br> *e.g: myGenes.txt*
| -dataset | *It defines the dataset* | exac, gnomad_r2_1, gnomad_r3, gnomad_r2_1_controls, gnomad_r2_1_non_neuro, gnomad_r2_1_non_cancer, gnomad_r2_1_non_topmed
| -h | It displays the parameters | *To get help via script:* `python gnomad_python_api.py -h`

## :hash: Example Usages
- **How to list the variants by gene name or gene id?**

`python gnomad_python_api.py -filter_by="gene_name" -search_by="TP53" -dataset="gnomad_r2_1"`

> Here,  "**gene_id**" can also be used instead of "**gene_name**" after stating an **Ensembl Gene ID** instead of a gene name.

- **How to list the variants by transcript ID?**

`python gnomad_python_api.py -filter_by="transcript_id" -search_by="ENST00000544455" -dataset="gnomad_r3"`

- **How to list the variants using a file containing genes/transcripts?**

  - Prepare your file that contains gene name, Ensembl gene IDs or Ensembl transcript IDs line-by-line. 
	> ENSG00000169174 <br> ENSG00000171862  <br> ENSG00000170445

  - Then, run the following command:
  
  `python gnomad_python_api.py -filter_by="gene_id" -search_by="myFavoriteGenes.txt" -dataset="exac"`

> Please, use only one type of identifier in the file.

- Then, the variants will be listed in "**outputs**" folder in the files according to their identifier (gene name, gene id or transcript id).  
-  That's all!

## :hash: Contributing & Feedback
I would be very happy to see any feedbacks and contributions on the script.

**Furkan Torun |  [furkanmtorun@gmail.com](mailto:furkanmtorun@gmail.com) | Website: [furkanmtorun.github.io](https://furkanmtorun.github.io/)**



