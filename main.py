import webbrowser
import pyautogui
import time
import pyperclip
import json
from datetime import datetime



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

            
job = jobFinder()
job.main()



