import os
import ast
import glob
import pdfplumber
import pandas as pd
import anthropic
from dotenv import load_dotenv
from typing import List, Dict
from datetime import datetime
from constants import SYS_EXTRACTION_PROMPT

load_dotenv()

class LLMExtractionPipeline():
    def __init__(self,
                 data_path:str=f'{os.getcwd()}\\data\\raw\\'):
        self.client = anthropic.Anthropic()
        self.raw_data_path = data_path
        print(f'{datetime.now()}: Pipeline started')


    def list_all_files(self,simbol:str)->List[str]:

        '''
        List all files of quartely reports
        Simbols allowed == REXP or DIPD
        '''
        
        try:
            return [glob.glob(
                f'{self.raw_data_path}\\{simbol}\\{file}')[0] \
                    for file in os.listdir(f'{self.raw_data_path}{simbol}')]
        except FileNotFoundError:
            raise BaseException(
                'Error on listing files: Simbol not found! Simbols allowed REXP or DIPD')

    def extract_pl_pages(self,simbol:str)->str:

        '''Extract the P&L pages'''
        financial_files = self.list_all_files(simbol)
        target = {
            'index':[],
            'simbol':[],
            'file_name':[],
            'target_page':[]}
        
        map_page_simbol = {
            'REXP':'Consolidated Income Statements',
            'DIPD':'STATEMENT OF PROFIT OR LOSS'
        }
        index = 0
        for financial_file in financial_files:
            
            with pdfplumber.open(financial_file) as pdf:
        
                for page_num, page in enumerate(pdf.pages):
        
                    if  map_page_simbol.get(simbol) in page.extract_text():
                        target['simbol'].append(simbol)
                        target['file_name'].append(financial_file[financial_file.find(simbol)+5:])
                        target['target_page'].append(page.extract_text())
            target['index'].append(index)
            index+=1
        return target

    def llm_data_extraction(
            self,
            pages:List[Dict[str,str]],
            sys_prompt:str,
            model_name:str="claude-sonnet-4-20250514",
            max_tokens:int=4096)->List[str]:
        
        '''Let Claude extract and format correct data from statement pages'''
        
        responses = []
        
        for index in range(len(pages['index'])):
            message = '{\n'
            
            for key,value in pages.items():
                message+=f'''
                    "{key}":"{value[index]}",'''
            message+='\n}'
            response = self.client.messages.create(
                model=model_name,
                max_tokens=max_tokens,
                system=sys_prompt,
                messages=[
                    {'role':'user','content':message}
                ])
            responses.append(response.content[0].text)
        
        return responses

    def parse_llm_extraction_response(
            self,
            responses:List[str])->List[Dict[str,str]]:
        '''Helper function to ensure data format as a json literal eval'''
        datas =[]
        for data in responses:
            parsed = data.replace('```','').replace('json','')
            try:
                datas.append(ast.literal_eval(parsed))
            except Exception as e:
                print(parsed)
                raise e
        return datas

    def run(
            self,
            target_folder: str = f'{os.getcwd()}\\data\\processed\\',
            output_filename: str = 'financial_data.csv'):
        
        # Scrap pdf's
        print(f'{datetime.now()}: Extracting statement pages from pdf files...')
        pl_pages_rexp = self.extract_pl_pages('REXP')
        pl_pages_dipd = self.extract_pl_pages('DIPD')

        print(f'{datetime.now()}: Extracting data from statement pages...')
        responses_dipd = self.llm_data_extraction(
            pages=pl_pages_dipd, sys_prompt=SYS_EXTRACTION_PROMPT)
        responses_rexp = self.llm_data_extraction(
            pages=pl_pages_rexp, sys_prompt=SYS_EXTRACTION_PROMPT)

        # Handle data
        print(f'{datetime.now()}: Ensure correct data format...')
        parsed_dipd_data = self.parse_llm_extraction_response(responses_dipd)
        parsed_rexp_data = self.parse_llm_extraction_response(responses_rexp)
        
        print(f'{datetime.now()}: Mounting Dataframe...')
        df = pd.concat(
            (pd.DataFrame(parsed_dipd_data),
            pd.DataFrame(parsed_rexp_data))
            ).reset_index().drop('index', axis=1).drop('level_0', axis=1)
        
        dates = []
        for value in df['file_name'].str.replace('.pdf', '').values:
            report_date = datetime.strptime(value, '%d%m%Y')
            dates.append(report_date)
        
        df['Report Date'] = dates
        df = df.sort_values(['Report Date']).reset_index().drop('index', axis=1)
        
        # Saving output
        os.makedirs(target_folder, exist_ok=True)
        output_path = os.path.join(target_folder, output_filename)
        
        try:
            print(f'{datetime.now()}: Saving Dataframe at {output_path}...')
            df.to_csv(output_path, index=False)
            print(f'{datetime.now()}: File saved successfully!')
            
        except Exception as e:
            print(f'{datetime.now()}: Fatal error while saving file! {e}')
            raise e
            
if __name__ == '__main__':
    pipeline = LLMExtractionPipeline()
    pipeline.run()