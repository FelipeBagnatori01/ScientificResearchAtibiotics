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
print(df)
