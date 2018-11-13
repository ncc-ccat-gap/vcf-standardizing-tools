# vcf-standardizing-tools

## INSTALL

### Document
picard (liftover)  
https://broadinstitute.github.io/picard/command-line-overview.html#LiftoverVcf  
bcftools (norm)    
https://samtools.github.io/bcftools/bcftools.html#norm  

### Install picard
git clone https://github.com/broadinstitute/picard.git  
cd picard   
docker build -t picard .  

### Install bcftools 
wget https://github.com/samtools/bcftools/releases/download/1.9/bcftools-1.9.tar.bz2  
tar yxvf bcftools-1.9.tar.bz2  
make  
make install  

### Install htslib  
http://www.htslib.org/download/  
tar yxvf htslib-1.9.tar.bz2  
make  
make install  

### Get chain file (Please refer to the credits)   
wget http://hgdownload.soe.ucsc.edu/goldenPath/hg19/liftOver/hg19ToHg38.over.chain.gz  
guzip hg19ToHg38.over.chain.gz  

### Get Reference genome  
https://gdc.cancer.gov/about-data/data-harmonization-and-generation/gdc-reference-files  
GRCh38.d1.vd1.fa.tar.gz  

### Create Reference dictionary
    docker run \
    -v /Users/chibaken/top-gear-vcf-check/ref:/local/ref \
    picard CreateSequenceDictionary \
    R=/local/ref/GRCh38.d1.vd1.fa \
    O=/local/ref/GRCh38.d1.vd1.dict


## Run

### VCF standardization
    cd /Users/chibaken/top-gear-vcf-check/tools/liftover_test/script  
    python standard_vcf_mutation.py mutation.vcf mutation_standard.vcf  

### liftover
    docker run \
    -v /Users/chibaken/top-gear-vcf-check/ref:/local/ref \
    -v /Users/chibaken/top-gear-vcf-check/output:/local/output \
    picard -j "-Xmx8000m" LiftoverVcf \
    I=mutation_standard.vcf \
    O=mutation_liftover.vcf \
    CHAIN=/local/ref/hg19ToHg38.over.chain \
    REJECT=mutation_reject.vcf \
    R=/local/ref/GRCh38.d1.vd1.fa

### VCF sort
    bcftools sort mutation_liftover.vcf > mutation_sorted.vcf

### Normalize indels
    bcftools norm \
    --fasta-ref GRCh38.d1.vd1.fa \
    mutation_sorted.vcf > mutation_normalize.vcf

### VCF check
    bash run_vcf-validator.sh vcf-validator \
    mutation_normalize.vcf \
    output_dir/check_result

### bgzip and create index
    bgzip mutation_normalize.vcf
    tabix -p vcf mutation_normalize.vcf.gz

