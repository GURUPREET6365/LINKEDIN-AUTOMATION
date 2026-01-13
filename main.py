import webbrowser
import pyautogui
import time
import pyperclip
import json
from dotenv import load_dotenv
from datetime import datetime
from google import genai
import os

load_dotenv()


# first = coordinates[0]['start_job_page']['x']
# print(first)


class jobFinder:
    def __init__(self):
        print('Now opening the website...')
        self.url = "https://www.linkedin.com/jobs/search/?keywords=Data%20Scientist"
        webbrowser.open(self.url)
        print('Website has been opened.')

    def selection_text(self):
        self.start = {'x':630,'y':319}
        # Move to start position
        # print('clicking at the starting point')
        pyautogui.moveTo(self.start['x'], self.start['y'], duration=0.3)
        pyautogui.click()
        time.sleep(0.3)
        pyautogui.scroll(20)
        time.sleep(2)

        # Start selection
        pyautogui.mouseDown()
        time.sleep(1)

        # Initial small drag to start selecting text
        pyautogui.moveTo(self.start['x'], self.start['y'] + 30, duration=0.2)

        # Scroll while holding mouse button
        for _ in range(8):
            pyautogui.scroll(-300)   # scroll DOWN
            time.sleep(1)

        # End selection
        pyautogui.mouseUp()
        time.sleep(0.3)

        # Copy
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.5)
        self.text = pyperclip.paste()

        self.clean_text = self.text.replace("\r\n", "\n").strip()

        pyautogui.click(x=632, y=381)
        time.sleep(0.7)
    



    def is_url_exists(self):
        pyautogui.moveTo(x=630, y=319)
        pyautogui.click()

        print('Copying the url....')

        pyautogui.hotkey("ctrl", "l") # This is hot key for copying the url
        time.sleep(0.2)

        # Copy URL
        pyautogui.hotkey("ctrl", "c")
        time.sleep(0.2)

        self.url = pyperclip.paste()

        print('now checking the url that is this exists.')

        try:
            with open('raw_data.json', 'r', encoding="utf-8") as reading_file:
                self.file = json.load(reading_file)
        
        except FileNotFoundError:
            print('File not found.')
            return False
        except Exception as error:
            print('The error found is:', error)
            return False

        if not self.file['jobs']:
            print('first urls so not checking that.')
            return True
        


        else:
            for job in self.file['jobs']:
                existing_url = job['url']
                # Here i am checking that if the url is exists return false.
                if self.url == existing_url:
                    print('The url is found same, so i am not storing that.', self.url)
                    return False
                
            print('urls is safe not found in the file......') 
            return True

        # """
        # for job in self.file['jobs']:
        #     existing_url = job['url']
        #     # Here i am checking that if the url is exists return false.
        #     if self.url == existing_url:
        #         print('The url is found same, so i am not storing that.', self.url)
        #         return False
            
        #     else:
        #         print('urls is safe not found in the file......')
        #         return True


        # HERE THE PROBLEM IS: 
        # I did it right but returning too early and that's why the single url is not checking the rest of url than first url.
        # """

    def raw_data_add(self):
        
        # print(file['jobs'])
        """
        print(file)
        Output is: 
        {'jobs': []}

        print(file['jobs'])
        Output is:
        []

        if file is empty...
        """ 

        # Now i am checking the length of the list so that i can give the new number.
        length = len(self.file['jobs'])+1
        # print(length)

        # print('printing the lenght of the data...')
        
        text = {
            'id':length,
            'url':self.url,
            'raw_text':self.clean_text,
            'timestamp':datetime.now().isoformat()
        }

        self.file['jobs'].append(text)

        # Now dumping the file...
        with open('raw_data.json', 'w', encoding='utf-8') as to_save_file:
            json.dump(self.file, to_save_file, indent=2, ensure_ascii=False)


    def scroll(self):
        time.sleep(1)
        pyautogui.moveTo(x=224, y=328)  # Target scroll area
        time.sleep(0.3)
        pyautogui.scroll(-70)
        time.sleep(1)
        pyautogui.click()
        time.sleep(1)


    def main(self):
        time.sleep(10)
        for x in range(35):
            time.sleep(2)
            if self.is_url_exists():
                self.selection_text()
                self.raw_data_add()

            self.scroll()
        
        for _ in range(20):
            pyautogui.click(x=541, y=528)

            pyautogui.moveTo(x=630, y=319)
            pyautogui.click()
            """
            Above I am clicking this because when new pages are loaded then i doest not go to the top from where it had to select.
            """
            for _ in range(8):
                pyautogui.scroll(300)   # scroll DOWN
                time.sleep(0.2)

            self.main()

    
    def is_url_exists_in_information_json(self):
        try:
            with open('raw_data.json', 'r', encoding="utf-8") as reading_file:
                self.url_stored_file = json.load(reading_file)
                """
                This is the file where raw data is stored with it's url and now i am going to give them url.
                """
        
        except FileNotFoundError:
            print('File not found.')
            return False
        except Exception as error:
            print('The error found is:', error)
            return False
        
        try:
            with open('information.json', 'r', encoding="utf-8") as reading_file:
                self.url_checking_file = json.load(reading_file)

                """
                This is the file where the new data will stored.
                """

        except FileNotFoundError:
            print('File not found.')
            return False
        except Exception as error:
            print('The error found is:', error)
            return False
        
        if not self.url_stored_file['jobs']:
            print('The raw_data.json file is null.')
            return False
        
        elif not self.url_checking_file['jobs_information']:
            self.url_to_give_to_ai = []
            print(self.url_checking_file['jobs_information'])
            print('The information.json file is null.')
            self.url_to_give_to_ai = []
            for raw_data_url in self.url_stored_file['jobs']:
                old_url = raw_data_url['url']
                self.url_to_give_to_ai.append(old_url)
            return True

        else:
            
            url_in_information_json =[ item['url'] for item in self.url_checking_file['jobs_information']]

            """
            This is the form of the loop liek:
            for item in self.url_checking_file['jobs_information']:
                item['url']
            """

            self.url_to_give_to_ai = []
            for raw_data_url in self.url_stored_file['jobs']:
                old_url = raw_data_url['url']
                if old_url not in url_in_information_json:
                    self.url_to_give_to_ai.append(old_url)

                
                
            return True
                    

    def ai_Models(self):
        all_models = ['gemini-2.5-flash', 'gemini-2.5-pro', 'gemini-2.5-flash-lite','gemini-3-flash']

        all_api_key = [f'{os.getenv('GEMINI_API_KEY2')}', f'{os.getenv('GEMINI_API_KEY1')}', f'{os.getenv('GEMINI_API_KEY3')}']

        for json in self.url_stored_file['jobs']:
            if json['url'] in self.url_to_give_to_ai:

                for model in all_models:
                    
                    for api in all_api_key:
                        print(api)
                        client = genai.Client(api_key=api)
                        
                        try:
                            response = client.models.generate_content(
                                model=f"{model}", contents=f"""You are an information extraction system.

                                    Your task is to extract structured data from the given job description.

                                    STRICT RULES:
                                    - Return ONLY valid JSON.
                                    - Do NOT include explanations, comments, markdown, or extra text.
                                    - Do NOT hallucinate information.
                                    - If a field is not explicitly present, use null.
                                    - Skills must be a list of strings.
                                    - Keep values concise and factual.

                                    INPUTS:
                                    1) Job description text
                                    2) Extraction timestamp (ISO 8601 format)

                                    FIELDS TO EXTRACT:
                                    - company_name
                                    - company_address
                                    - posted_days_ago
                                    - skills (list)

                                    JOB DESCRIPTION:
                                    {json['raw_text']}"""
                                    )
                            
                            if response.text:
                                print('found the response from ai that is')
                                # Now i am checking that the ai response is, is json or not.
                                strip_text = self.clean_ai_json(response.text)
                                is_valid_data, data = self.is_json_response(strip_text)
                                if is_valid_data:
                                        data["id"] = json['id']
                                        data["url"] = json["url"]
                                        data["timestamp"] = json["timestamp"]
                                        data["extracted_at"] = datetime.now().isoformat()

                                        self.save_ai_response_into_information_file(data)     
                                        time.sleep(38)     
                                        break                         

                        except Exception as error:
                            print('The error is:', error)
                            time.sleep(38)
                            continue


    def clean_ai_json(self, text) -> str:
        text = text.strip()

        # Remove ```json or ```
        if text.startswith("```"):
            text = text.strip("`")
            text = text.replace("json", "", 1).strip()

        return text


                    
    def is_json_response(self, text):
        try:
            data=json.loads(text)
            return True, data
        # Here i am returning two data so the python will return tuples.
        except json.JSONDecodeError:
            return False, None


    def save_ai_response_into_information_file(self, data):
        try:
            with open('information.json', 'r', encoding="utf-8") as reading_file:
                self.information_json = json.load(reading_file)

                """
                This is the file where the new data will stored.
                """

                self.information_json['jobs_information'].append(data)

                with open('information.json', 'w', encoding='utf-8') as to_save_file:
                    json.dump(self.information_json, to_save_file, indent=2, ensure_ascii=False)

        except FileNotFoundError:
            print('File not found.')
            return False
        except Exception as error:
            print('The error found is:', error)
            return False

    def ai_process(self):
        if self.is_url_exists_in_information_json():
            self.ai_Models()


# job = jobFinder()
# job.main()

# job.ai_process()

