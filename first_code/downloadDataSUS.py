import pandas as pd

from pysus.ftp.databases.sih import SIH

def downloadData(uf, years, months, local_dir, group="RD"):
    sih = SIH().load()
    df = pd.DataFrame(data={})
    
    for year in years:
        files = sih.get_files(group, uf=uf, year=year, month=months)
        parquet = sih.download(files, local_dir=local_dir)
        df0 = parquet[0].to_dataframe()
        for i in range(1, len(files)):
            dfAux = parquet[i].to_dataframe()
            df0 = pd.concat([df0, dfAux], ignore_index=True)
        df = pd.concat([df, df0], ignore_index=True)
    
    return df

df = downloadData("SP", [2020, 2021], [1, 2, 3], "/Users/febagnatori/Documents/GitHub/ScientificResearchAtibiotics/Dados")
#df.to_csv('out.csv')
var_interesse = [
    "ANO_CMPT", "MES_CMPT", "CGC_HOSP", "N_AIH", "CEP", 
    "NASC", "SEXO", "UTI_MES_TO", "MARCA_UTI", "PROC_SOLIC", "PROC_REA", "VAL_SH", "VAL_SP", 
    "VAL_TOT", "VAL_UTI", "DT_INTER", "DT_SAIDA", "DIAG_PRINC", "DIAG_SECUN", "IND_VDRL", 
    "MUNIC_MOV", "COD_IDADE", "IDADE", "MORTE", "NACIONAL", "INSTRU", "CBOR", 
    "CNES", "INFEHOSP", "CID_MORTE", "RACA_COR", "ETNIA", "DIAGSEC1", "DIAGSEC2", 
    "DIAGSEC3", "DIAGSEC4", "DIAGSEC5", "DIAGSEC6", "DIAGSEC7", "DIAGSEC8", "DIAGSEC9"
]
print(df.filter(var_interesse))
