# Každej Usecase je pod ucXYZ_config.toml
# Každej Usecase Generuje custom output z Generation.custom_output_attributes."např adresa pobočky"
# Každej Usecase jich má N a vždy to je nějakej string jako odpověď 

# V testu je to generované že zadají sadu otázek, odpovědi k tomu (initData) a generuje se AI odpověď (Data) + info jestli uživatel zasáhnul a musel to opravit
# V produkci je to už jen jako Querry a výstup AI + info jestli je feedback ok a nebylo to potřeba měnit

# Nechci asi jít cestou, že každej Usecase object může mít další podobjekty jako usecase 1, usecase 1.1, 1.2, 1.3 ...? (možná jít)


# feedback_collector pro jejich usecase na dokumenty
#       id,user,createddate,starteddate,completeddate, confirmeddate, closedate, State (nvm co je state), canceleddate, modifieddate, sourcefilename, sourcefilecontent, sourcefilelocal path, ProcessTypeId (důležitý), InitialData, Data (oba důležitý), AnnotatedFilePath, Note, ModuleId
# feedback_collector pro jejich pob. asistenta  
#       Samé columns, akorát je tam jen Querry, z čeho tahá, Odpověď-AI, User satysfactory y/n
from typing import Dict, Any, List
from pathlib import Path
import pandas as pd
import json

GLOBAL_PATH = "database_pokus.csv"

class FeedbackCollector:
    def __init__(self, config: Path):
        self.config = config
        self.loader = DataLoader()
    pass

class DataLoader:
    def __init__(self, file_path: Path):
        self.csv_path = file_path
        self.raw_data = None
        self.json_columns = []
        
    def load_csv(self, sep=";", quotechar='"', **kwargs) -> pd.DataFrame:
        try:
            self.raw_data = pd.read_csv(self.csv_path, sep=sep, quotechar=quotechar, **kwargs)
            print(f"## Loaded number of recors: {len(self.raw_data)}## From file: {self.csv_path}")
            return self.raw_data
            
        except Exception as e:
            raise Exception(f"Failed loading file: {e}")
    
    def normalize_json_cols(self, cols: List[str]) -> pd.DataFrame:
        if self.raw_data is None:
            raise ValueError("Value Error")
        for col in cols:
            try:
                parsed = self.raw_data[col].dropna().apply(json.loads)
                
                normalized = pd.json_normalize(parsed)
                normalized.columns = [f"{col}_{c}" for c in normalized.columns]
                
                
                self.raw_data = self.raw_data.drop(columns=[col])
                self.raw_data = pd.concat([self.raw_data, normalized], axis=1)
            except Exception as e:
                print(f"Error with col '{col}': {e}")
            
        return self.raw_data
    
    def data_process(self, json_cols: List[str], **csv_kwargs) -> pd.DataFrame:
        self.load_csv(**csv_kwargs)
        self.normalize_json_cols(json_cols)
        
        return self.raw_data

class ColExtractor:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        pass
    
    def select_cols():
        pass
    
    def extracted_cols():
        pass
    
class DataMetrics:
    def __init__(self):
        pass
    
class DataExporter:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        
        pass

loader = DataLoader(Path(GLOBAL_PATH))
df_class = loader.data_process(json_cols=["InitialData", "DataAI"])

df = pd.read_csv(GLOBAL_PATH, sep=";", quotechar='"')
print(f"Normální DF columns: {df.columns}, Normální DF shape: {df.shape}")


print(f"Tohle jsou columns po loadingu:{df_class.columns}")
print(df["InitialData"])
print(df["DataAI"])

# Pro ten celkový usecase má ještě maping pro 4 další pod-uscase MAPPING ve tvaru 1: "Kupní smlouva", 2: "Nájemní smlouva" atd..
# File setup Global proměnný
# Excel setup Global proměnný

# Extrakce Columns, převod Datumu na správný formát, row_data = {ID row['Id']}
# Přídání new column podle toho, jestli DataInit (user) == Data (AI) když jo OK, když ne KO, a pokud je aspoň jedno KO, tak addnout nakonec colum s KO
#  

print(f"Pokus o write Excelu")
excel_print = df_class.to_excel(excel_writer="kebabmore.xlsx", sheet_name="Jebka Jedna")
print("Asi jsem printunl?", excel_print)