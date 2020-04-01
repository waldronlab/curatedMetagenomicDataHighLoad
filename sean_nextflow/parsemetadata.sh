#!/usr/bin/env Rscript --vanilla

if(!suppressPackageStartupMessages(require("docopt"))){
  stop("You must have the docopt R package installed. Assuming you have
             installed R & Bioconductor (www.bioconductor.org/install), type:\n
             BiocInstaller::biocLite(\"docopt\") \n
             from your R prompt.")
}

"Usage: parsemetadata.R [-hf FILE]

-h --help    show this
-f FILE      specify curated metadata file (e.g. see https://github.com/waldronlab/curatedMetagenomicDataCuration/blob/master/inst/curated/AsnicarF_2017/AsnicarF_2017_metadata.tsv" -> doc

input <- docopt(doc)

fname <- input[["-f"]]
tab <- read.delim(fname, as.is=TRUE)

zz <- stdout()
sink(zz)

cat(paste0("#", sub("_metadata.tsv", "", basename(fname))))
for (i in seq(nrow(tab))){
  line <- paste0("bash curatedMetagenomicData_pipeline.sh ", 
         tab[i, "subjectID"], 
         ' "',
         tab[i, "NCBI_accession"],
         '"\n')
  cat(line)
}
