import sys

in_vcf = sys.argv[1]
out_vcf = sys.argv[2]

hout = open(out_vcf, 'w')
print >> hout, '##fileformat=VCFv4.2'
print >> hout, '##ALT=<ID=CNV,Description="Copynumbervariableregion">'

with open(in_vcf, 'r') as hin:
    for line in hin:
        line = line.rstrip('\n')

        # print meta 
        if line.startswith("##"):
            if(line.startswith("##INFO=<ID=END") or \
              line.startswith("##INFO=<ID=SVLEN") or \
              line.startswith("##INFO=<ID=SVTYPE") or \
              line.startswith("##INFO=<ID=CNVTYPE") or \
              line.startswith("##INFO=<ID=BGDP") or \
              line.startswith("##INFO=<ID=AMPLOGR") or \
              line.startswith("##INFO=<ID=NEULOGR") or \
              line.startswith("##INFO=<ID=DELLOGR") or \
              line.startswith("##INFO=<ID=AMPCOV") or \
              line.startswith("##INFO=<ID=NEUCOV") or \
              line.startswith("##INFO=<ID=DELCOV") or \
              line.startswith("##contig=") or \
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
                if info.startswith("END=") or \
                  info.startswith("SVLEN=") or \
                  info.startswith("SVTYPE="):
                    new_info.append(info)
            
            format_fields = F[8].split(':')
            format_data_fields = F[9].split(':')
            for idx in range(len(format_fields)):
                format = format_fields[idx]
                if format.startswith("CNVTYPE") or \
                  format.startswith("BGDP") or \
                  format.startswith("AMPLOGR") or \
                  format.startswith("NEULOGR") or \
                  format.startswith("AMPCOV") or \
                  format.startswith("NEUCOV") or \
                  format.startswith("DELCOV"):
                    data = format_data_fields[idx]
                    new_info.append(format +"="+ data)

            print >> hout, "\t".join(F[0:2])+"\t.\t"+"\t".join(F[3:5])+"\t.\t"+F[6]+"\t"+";".join(new_info)
            
hout.close()
