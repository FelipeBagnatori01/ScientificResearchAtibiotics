# IMPORTANDO PACOTES 
import pandas as pd   

from ftplib import FTP
from pysus.online_data.SIH import download

#DEFININDO VARIÁVEIS QUE SERÃO USADAS NO DOWLOAD DOS DADOS

#DEFININDO VARIÁVEIS
vars = ["MORTE", "CID_MORTE", "DIAG_PRINC"]
ufs = ["df"]
anos = [2021] 
meses = [ 11, 12] 
cids = ["J13", "J14"]
grupos = ['RD', 'RJ', 'ER', 'SP', 'CH', 'CM',]


#IMPORTANDO DADOS
for mes in meses: 
    for uf in ufs:
        for ano in anos:   
            d = download(uf, ano, mes, grupos,
                         data_dir="/Users/febagnatori/Documents/GitHub/ScientificResearchAtibiotics/Dados")
            frames = [d[i].to_dataframe() for i in range(0, len(d))]
            df = pd.concat(frames)
            df = df.filter(vars)
            print(df)
            df.to_csv("sih_pneumonia_20_21.csv", mode='a', index=False, header=False)
            print(f"O arquivo do mês {mes} de {ano} do estado {uf.upper()} foi filtrado")