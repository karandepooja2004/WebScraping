# Scraping Business Details using Python
**Project Overview**
  
  This project collects business information across multiple categories and regions using the Google Places API. 
  The extracted data includes:
   
    Business Name
    Phone Number
    Website
    Address
    Category
    (Email, where available)
    
  The final data is saved into an Excel file, categorized and structured for ease of analysis.


**Data Sources**

**1. Google Places API**

  **Text Search API:** Used to find businesses by category and region.
  
  **Place Details API:** Used to fetch additional details (phone number, website, etc.).


**2. Missing / Limited Categories**

  Some categories may have fewer than 10 businesses in certain regions due to limited availability. 
  
  **Examples:**
  
    Jewelry & Accessories
    Furniture & Décor
    Coaching Institutes
    Catering Services
    Businesses in remote regions 
    
  For transparency, a note “Less than 10 records available” is added to the excel wherever applicable.
  

**Challenges Faced**

**1. Billing & Quota Management**

  The Google Places API requires an active billing account, even for free-tier credits.
  
  Each business record requires multiple API calls (Text Search + Place Details), so quota usage had to be carefully managed.


**2. Email Extraction Limitations**

The API does not provide email addresses. Email scraping from business websites is inconsistent because some websites use forms instead of direct contact info, Certain sites restrict or block automated scraping.


**Output Delivered**

  **Excel File (e.g., Kansas_Business.xlsx)**
  
    Contains categorized business records.
    Each region can be saved on a separate sheet.
    Validation included for missing/limited categories. If any category have less than 10 records then a note “Less than 10 records available for this Category” is added to the excel. 
