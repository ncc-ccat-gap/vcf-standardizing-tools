import sys

in_vcf = sys.argv[1]
out_vcf = sys.argv[2]

hout = open(out_vcf, 'w')
print >> hout, "##fileformat=VCFv4.2"

with open(in_vcf, 'r') as hin:
    for line in hin:
        line = line.rstrip('\n')

        # print meta 
        if line.startswith("##"):
            if line.startswith("##FILTER=") or \
              line.startswith("##INFO=<ID=AF,") or \
              line.startswith("##INFO=<ID=DP,") or \
              line.startswith("##contig=") or \
              line.startswith("##reference=") or \
              line.startswith("##source="):
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
                  info.startswith("DP="):
                    new_info.append(info)

            print >> hout, "\t".join(F[0:2])+"\t.\t"+"\t".join(F[3:5])+"\t.\t"+F[6]+"\t"+";".join(new_info)
            
hout.close()
