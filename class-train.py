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
        
    def load_csv(self, sep=";", quotechar='"', **kwargs) -> pd.DataFrame:
        try:
            df = pd.read_csv(self.csv_path, sep=sep, quotechar=quotechar, **kwargs)
            print(f"## Loaded number of records: {len(df)}## From file: {self.csv_path}")
            return df
            
        except Exception as e:
            raise Exception(f"Failed loading file: {e}")
    

class DataTransformer:
    def __init__(self, df: pd.DataFrame):
        self.df = df
    
    def normalize_json_cols(self, cols: List[str], fields_per_col: Dict[str, List[str]] = None) -> pd.DataFrame:
        if self.df is None:
            raise ValueError("Data didn't load")
        
        
        for col in cols:
            try:
                parsed = self.df[col].dropna().apply(json.loads)
                
                if fields_per_col and col in fields_per_col:
                    # selectively extracting the json fields
                    parsed  = parsed.apply(lambda d: {k: d.get(k) for k in fields_per_col[col]})
                    
                
                normalized = pd.json_normalize(parsed)
                normalized.columns = [f"{col}_{c}" for c in normalized.columns]
                
                
                self.df = self.df.drop(columns=[col])
                self.df = pd.concat([self.df, normalized], axis=1)
            except Exception as e:
                print(f"Error with col '{col}': {e}")
            
        return self.df

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
df = loader.load_csv()
transformer = DataTransformer(df)
#df_class = loader.data_process(json_cols=["InitialData", "DataAI"])

df_transformed = transformer.normalize_json_cols(cols=["InitialData", "DataAI"],
    fields_per_col={
        "InitialData": ["Title", "Answer"],
        "DataAI": ["Answer"]
    }
)

print(f"Pokus o write Excelu")
excel_print = df_transformed.to_excel(excel_writer="kebabmore.xlsx", sheet_name="Jebka Jedna")
print("Asi jsem printunl?", excel_print)


df = pd.read_csv(GLOBAL_PATH, sep=";", quotechar='"')
print(f"Normální DF columns: {df.columns}, Normální DF shape: {df.shape}")


print(f"Tohle jsou columns po loadingu:{df_transformed.columns}")
print(df["InitialData"])
print(df["DataAI"])

# Pro ten celkový usecase má ještě maping pro 4 další pod-uscase MAPPING ve tvaru 1: "Kupní smlouva", 2: "Nájemní smlouva" atd..
# File setup Global proměnný
# Excel setup Global proměnný

# Extrakce Columns, převod Datumu na správný formát, row_data = {ID row['Id']}
# Přídání new column podle toho, jestli DataInit (user) == Data (AI) když jo OK, když ne KO, a pokud je aspoň jedno KO, tak addnout nakonec colum s KO
# Initial má Title: (Otázka) Answer: (Odpověď) a DataAI(Data) má taky Title: (Otázka) Answer: (Odpověď) if InitialData.Answer == DataAI.Answer OK else KO
# Pro každý ProcessTypeId novej Sheet (protože každej má jinak velký InitialData a DataAI)

# Nakonec udělat Jeden co shrne celkovou úspěšnost dokumentů a jednotlivých atributů

