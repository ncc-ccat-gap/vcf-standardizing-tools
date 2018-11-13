import sys

in_vcf = sys.argv[1]
out_vcf = sys.argv[2]

hout = open(out_vcf, 'w')
print >> hout, '##fileformat=VCFv4.2'
print >> hout, '##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">'
print >> hout, '##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">'
print >> hout, '##INFO=<ID=MATEID,Number=.,Type=String,Description="ID of mate breakends">'
print >> hout, '##INFO=<ID=TC,Number=1,Type=Integer,Description="Total number of reads with high quality for all methods">'
print >> hout, '##INFO=<ID=NF,Number=1,Type=Integer,Description="Number of non fusion reads with high quality">'
print >> hout, '##FILTER=<ID=LowQuality,Description="Low Quality">'
print >> hout, '##FILTER=<ID=PASS,Description="All filters passed">'

with open(in_vcf, 'r') as hin:
    for line in hin:
        line = line.rstrip('\n')

        # print meta 
        if line.startswith("##"):
            if(line.startswith("##contig=") or \
              line.startswith("##reference=") or \
              line.startswith("##source=")):
                print >> hout, line

        # print header
        elif line.startswith("#"):
            F = line.split('\t')
            print >> hout, "\t".join(F[0:8])
            # print >> hout, line
         
        # print body
        else:
            new_info = []
            F = line.split('\t')
            info_fields = F[7].split(';')
            for info in info_fields:
                if info.startswith("AF=") or \
                  info.startswith("SVTYPE=") or \
                  info.startswith("MATEID=") or \
                  info.startswith("TC=") or \
                  info.startswith("NF="):
                    new_info.append(info)

            print >> hout, "\t".join(F[0:3])+"\t"+"\t".join(F[3:5])+"\t.\t"+F[6]+"\t"+";".join(new_info)
            
hout.close()
