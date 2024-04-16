# IMPORTANDO PACOTES 
import pandas as pd   

from pysus.ftp.databases.sih import SIH
sih = SIH().load()

files = sih.get_files("RD", uf="SP", year=2020, month=[1,2,3])
sih.download(files, local_dir="/Users/febagnatori/Documents/GitHub/ScientificResearchAtibiotics/Dados")
parquet = sih.download(files)[0]
df = parquet.to_dataframe()
print(df)

