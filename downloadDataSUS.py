# IMPORTANDO PACOTES 
import pandas as pd   

from pysus.ftp.databases.sih import SIH

def downloadData(uf, year, months, local_dir, group="RD"):
    sih = SIH().load()
    files = sih.get_files(group, uf=uf, year=year, month=months)
    parquet = sih.download(files, local_dir=local_dir)
    df = parquet[0].to_dataframe()
    for i in range(1, len(files)):
        dfAux = parquet[i].to_dataframe()
        df = pd.concat([df, dfAux], ignore_index=True)
    return df

df = downloadData("SP", 2020, [1, 2, 3], "/Users/febagnatori/Documents/GitHub/ScientificResearchAtibiotics/Dados")
#df.to_csv('out.csv')
print(df)
