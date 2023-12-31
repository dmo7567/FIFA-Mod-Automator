import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import random

used_numbers = []

def generate_random_number(used_numbers):
    """Generate a random number between 1 and 99 that is not in the used_numbers set."""
    while True:
        random_number = random.randint(1, 99)
        if random_number not in used_numbers:
            used_numbers.append(random_number)
            return random_number



def scrape_and_save_to_excel(url, output_file):
    # Send a GET request to the specified URL
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    }

    response = requests.get(url, headers=headers)

    
    
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Create a new Excel workbook and select the active sheet
        wb = Workbook()
        ws = wb.active
        
        # Find the first <body> element
        body = soup.find('body')
        
        # Find all <tr> elements within the <body>
        rows = body.find_all('tr')
        
        for row in rows:
            # Skip rows that are None
            if row is None:
                continue
            
            #NUMBER search
            rueckennummer_element = row.find('td', class_='rueckennummer')
            number = rueckennummer_element.find('div', class_='rn_nummer').text if rueckennummer_element else None
            number = int(number) if number and number != '-' else None
            
            # Check if the 'number' is '-' and replace it with a random number
            if number != '-' :
                used_numbers.append(number)
            if number == '-':
                number = generate_random_number(used_numbers)

            #Image URL search
            posrela_element = row.find('td', class_='posrela')

            img_url_element = posrela_element.find('img') if posrela_element else None
            img_url = img_url_element['data-src'] if img_url_element and 'data-src' in img_url_element.attrs else None

            #NAME search
            name_element = posrela_element.find('a') if posrela_element else None
            name = name_element.text if name_element else None
            
            # Extract the first word as first_name and the rest as last_name
            if name:
                name = name.strip()
                name_parts = name.split(' ', 1)
                first_name = name_parts[0] if name_parts else None
                last_name = name_parts[1] if len(name_parts) > 1 else None
            else:
                first_name = None
                last_name = None
            #POSITION search
            #position_element = positionTable.find_next('tr').find('td') if positionTable else None
            #position = position_element.text if position_element else None
            position_element = posrela_element.find('td', class_='hauptlink').find_next('tr').find('td') if posrela_element else None
            position = position_element.text.strip() if position_element else None
            
            zentriert_tds = row.find_all('td', class_='zentriert')

            # Extract data from the third td element (index 2)
            birth_date = zentriert_tds[1].text.strip() if len(zentriert_tds) > 2 else None

            zentriert_td = row.find('td', class_='zentriert')
            #birth_date_element = zentrient_td.find_next_siblings('td')[0] if zentrient_td else None
            #birth_date = birth_date_element.text if birth_date_element else None
            
            #NATION search
            nation_element = zentriert_td.find_next_siblings('td')[2].find('img') if zentriert_td else None
            nation = nation_element['alt'] if nation_element else None
            
            #HEIGHT search
            height_element = zentriert_td.find_next_siblings('td')[4] if zentriert_td else None
            height = height_element.text if height_element else None
            
            #STRONG_FOOT search
            strong_foot_element = zentriert_td.find_next_siblings('td')[5] if zentriert_td else None
            strong_foot = strong_foot_element.text if strong_foot_element else None
           
            #JOIN search
            join_date_element = zentriert_td.find_next_siblings('td')[6] if zentriert_td else None
            join_date = join_date_element.text if join_date_element else None
            
            #MARKET value
            value_element = row.find('td', class_='rechts')
            value = value_element.find('a').text if value_element and value_element.find('a') else None
            
            # Save the extracted data to the Excel sheet
            #ws.append([number, img_url, name, position, birth_date, nation, height, strong_foot, join_date, value])
            #if number and img_url and name and position and birth_date and nation and height and strong_foot and join_date and value:
            #    ws.append([number, img_url, first_name, last_name, position, birth_date, nation, height, strong_foot, join_date, value])
            # Save the extracted data to the Excel sheet
            if number and img_url and first_name and last_name and position and birth_date and nation and height and join_date and value:
                # Check if strong_foot is not 'right' or 'left' and set it to 'right'
                if strong_foot not in ['right', 'left']:
                    strong_foot = 'right'

                ws.append([number, img_url, first_name, last_name, position, birth_date, nation, height, strong_foot, join_date, value])

        
        # Save the workbook to the specified file
        wb.save(output_file)
        print(f"Data has been successfully scraped and saved to {output_file}")
    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")

# Prompt the user to input the URL
url_to_scrape = input("Enter the URL to scrape: ")
output_excel_file = 'output_data.xlsx'
scrape_and_save_to_excel(url_to_scrape, output_excel_file)
