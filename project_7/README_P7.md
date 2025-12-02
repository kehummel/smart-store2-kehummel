# Project 7
In Module 7, we bring everything together by creating a custom BI decision support project that reflects real-world business intelligence challenges. You'll define a specific business goal, build a BI solution using the skills and tools from previous modules, and present your insights effectively.

We explore the role of AI and data ethics in business intelligence, addressing how automated decision-making and data-driven insights must align with ethical principles and business goals.

This short module is intended to consolidate learning and prepare you for independent BI work.

## 1. The Business Goal
We are focusing on previous customers and how to increase revenue from them. Our goal is to decide which location has the most customers, which location has more recent customers, determine what these customers buy, and how much they spend in order to create promotions that will encourage our loyalty members to purchase items from our store more frequently.

## 2. Data Source
The original data source is from Denise Case: https://github.com/denisecase/smart-sales-raw-data/tree/main/data/raw
It was initially cleaned and prepared for projects earlier in this module. It resides in the folders for the other projects.

     smartstore2-kehummel
        ├── src
        │   └── data
        │       └── prepared
        |           ├──customers_prepared.csv
        |           ├── products_prepared.csv
        |           └── sales_prepared.csv

## 3. Tools Used
I used python through vscode to clean the data and create a data cube. I used Power BI to create my visuals and help create my analysis.

## 4. Workflow & Logic

### Preparing Data
First, I wanted to make sure the data was ready for the analysis I was about to complete. I made sure money amounts went to two decimal places, that dates were formatted correctly, and that all other numbers were set as integers.

I also made sure all duplicates were removed, because that was a problem I had with a previous module; not all duplicates had actually been removed.

I removed all accounts that had 0 purchases because our goal is to increase purchases made by pervious customers, not people who had not bought anything.

### Creating Cube
I wanted to have the data joined altogether systematically so I decided to make a multidimensional cube so that it would be easy to load my data in Power BI.

### Visuals & Analyzing Data
I loaded my cube into Power BI and used charts and graphs to dissect the data more. This not only gave me the ability to narrow down my analysis, but it also provided me with visuals that I could use to show my analysis.

## 5. Results (narrative + visualizations)
## 6. Suggested Business Action
## 7. Challenges
## 8. Ethical Considerations
