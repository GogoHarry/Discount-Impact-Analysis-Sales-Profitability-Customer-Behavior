# Discount-Impact-Analysis-Sales-Profitability-Customer-Behavior

![sales_can](https://github.com/user-attachments/assets/a00b262c-d870-4df0-828b-7eb2a8c2a8bb)


## Project Overview
This Discount Impact Analysis project aims to evaluate the effectiveness of a recent 15% discount campaign launched by our tech company in January. The CEO has expressed concerns about the impact of the discount on profitability, and we need to analyze whether the discount is causing margin erosion or merely cannibalizing our full-price sales, as well as identify the customer segments influenced by the discount.

### Objectives
The key objectives of this project are:

1. Calculate the profitability impact of the discount.
2. Assess sales cannibalization.
3. Identify customer segments influenced by the discount.
4. Identify the best-performing product category.

By addressing these objectives, we aim to gain a comprehensive understanding of the effectiveness of our discount strategies and identify opportunities for improvement.

## Data Description

### Data Sources
The data analysis was performed using the following data sources:

1. **Transaction Data**: This dataset tracks customer purchases and applied discounts, with columns such as TransactionID, CustomerID, ProductID, Quantity, TotalAmount, and DiscountApplied.
2. **Customer Data**: This dataset contains customer demographic information, including CustomerID, Name, Gender, Email, and DateOfRegistration 
3. **Product Data**: This dataset holds details about the products being sold, including ProductID, ProductName, UnitPrice, Category, Stock, PopularityScore, ReturnRate, and CostPrice.

### Data Processing
The data was collected and processed using SQL queries in MySQL to prepare it for the analysis. This included tasks such as data cleaning, transformation, and aggregation to derive the necessary insights.

## Methodology

### Analytical Approach
The data analysis was conducted using a structured approach, focusing on the following areas:

1. **Profitability Impact**: Evaluating the overall impact of the discount on profitability.

```sql
-- Profitability Impact Analysis

SELECT 
    DATE_FORMAT(t.transactiontimestamp, '%Y-%m') AS salesmonth, 
    COUNT(*) AS totaltransaction, 
    AVG((p.unitprice - t.discount) - p.costprice) * t.quantity AS avgtransactionmargin, 
    SUM((p.unitprice - t.discount - p.costprice) * t.quantity) AS totaltransactionmargin 
FROM transaction t 
JOIN product p ON t.productpurchased = p.productid 
WHERE DATE_FORMAT(t.transactiontimestamp, '%Y-%m') IN ('2024-11', '2024-12', '2025-01') 
GROUP BY salesmonth 
ORDER BY salesmonth;
```
  
2. **Product Category Performance**: Identifying the best-performing product categories.

```
-- Product Category Performance

SELECT 
    DATE_FORMAT(t.transactiontimestamp, '%Y-%m') AS salesmonth,
    p.Category AS ProductCategory,
    COUNT(*) AS totaltransaction,
    AVG(((p.unitprice - t.discount) - p.costprice) * t.quantity) AS avgtransactionmargin,
    SUM(((p.unitprice - t.discount) - p.costprice) * t.quantity) AS totaltransactionmargin
FROM transaction t
JOIN product p ON t.productpurchased = p.productid
WHERE DATE_FORMAT(t.transactiontimestamp, '%Y-%m') IN ('2024-11', '2024-12', '2025-01')
GROUP BY salesmonth, ProductCategory
ORDER BY salesmonth, ProductCategory;
```

3. **Sales Cannibalization**: Assessing the potential for the discount to cannibalize full-price sales.

```sql

-- Sales Cannibalization Potential (do our customers buy only whenever there is discount?)

-- Create CTE
WITH CustomerActivity AS (
    SELECT 
        c.customerid, 
        c.name,  
        DATE_FORMAT(t.transactiontimestamp, '%Y-%m') AS salesmonth,
        COUNT(t.TransactionID) AS transactions
    FROM transaction t
    JOIN customer c ON t.customerid = c.customerid
    WHERE DATE_FORMAT(t.transactiontimestamp, '%Y-%m') IN ('2024-11', '2024-12', '2025-01')
    GROUP BY c.customerid, c.name, DATE_FORMAT(t.transactiontimestamp, '%Y-%m')
)

SELECT 
    ca.customerid, 
    ca.name,
    MAX(CASE WHEN ca.salesmonth IN ('2024-11', '2024-12') THEN ca.transactions ELSE 0 END) AS previous_transactions,
    MAX(CASE WHEN ca.salesmonth = '2025-01' THEN ca.transactions ELSE 0 END) AS january_transactions
FROM CustomerActivity AS ca
GROUP BY ca.customerid, ca.name
ORDER BY january_transactions DESC;
```

4. **Customer Segment Analysis**: Determining which customer segments were influenced by the discount.

```sql

-- Customer Segment Analysis (to know our loyal customers)

SELECT 
    DATE_FORMAT(t.transactiontimestamp, '%Y-%m') AS salesmonth,
    CASE
        WHEN c.DateofRegistration < DATE_FORMAT(t.transactiontimestamp, '%Y-%m') THEN 'returning_customers'
        ELSE 'new_customers' 
    END AS Customer_Type,
    COUNT(DISTINCT c.customerid) AS Customer_Count,
    COUNT(t.transactionid) AS Total_Transactions,
    SUM(t.Quantity) AS Total_Unit_Sold
FROM transaction t
JOIN customer c ON t.customerid = c.customerid
WHERE DATE_FORMAT(t.transactiontimestamp, '%Y-%m') IN ('2024-11', '2024-12', '2025-01')
GROUP BY salesmonth, Customer_Type
ORDER BY salesmonth, Customer_Type;
```

### Tools and Techniques
The insights from this analysis were generated using SQL queries in MySQL and visualized using PowerBI to create an interactive dashboard.

## Results

### Profitability Impact
The analysis revealed that the total profit increased by 15% during the discount period, suggesting that the discount campaign was effective in driving sales and revenue growth. However, further investigation is needed to determine if this increase in profit is sustainable or if it's being driven by the discount itself, which could lead to margin erosion in the long run.

![image](https://github.com/user-attachments/assets/d39bc5b3-d4e6-4e1d-86ee-454f082d0ef7)

### Sales Cannibalization
The analysis showed that certain customer segments exhibited a significant increase in transactions during the discount period, indicating potential sales cannibalization. This means that the discount may have attracted customers who would have purchased at full price, leading to a decrease in overall profitability. We need to carefully examine the impact on different customer segments to ensure we're not sacrificing long-term profitability for short-term sales gains.

![image](https://github.com/user-attachments/assets/db5676ab-f56a-4372-871b-b1fb7643bdf5)

### Best Performing Product Category
The analysis revealed that the Electronics category contributed over 60% to overall profitability, while the Books category was more sensitive to margin erosion. This insight suggests that we should prioritize high-margin product categories in our discount strategy, while evaluating the impact on less profitable categories.

![image](https://github.com/user-attachments/assets/f4da13c4-2c77-43a5-a348-2c1fe87a9f9e)


### Customer Segment
The analysis also showed that new customer acquisition declined during the discount period, indicating that the discount was more effective in attracting existing customers rather than acquiring new ones. This finding highlights the importance of refining our customer segmentation and marketing strategies to better target and retain the most profitable customer segments.

![image](https://github.com/user-attachments/assets/2d3e314d-c4fb-4183-853a-e0add10efc0e)


## Conclusion
This Discount Impact Analysis project has provided us with valuable insights to optimize our discount strategies and drive sustainable growth. By implementing the recommended actions, we can address the identified challenges and ensure the long-term profitability of our ecommerce business.

## Recommendations
Based on the insights from our analysis, we recommend the following actions:

1. Implement targeted promotions and loyalty programs to incentivize full-price purchases and retain high-value customers.
2. Refine customer segmentation and marketing strategies to better attract and retain the most profitable segments.
3. Prioritize high-margin product categories in the discount strategy, while evaluating the impact on less profitable categories.
4. Continuously monitor the profitability impact and adjust the discount approach to balance sales growth and overall profitability.

## Future Work
While this Discount Impact Analysis project has provided us with valuable insights, there are still potential areas for further analysis or improvement:

1. Expand the analysis to include additional data sources, such as marketing campaigns and external market trends.
2. Develop more sophisticated customer segmentation models to better target high-value segments.
3. Explore dynamic pricing strategies to optimize discounts based on real-time market conditions.

By addressing these areas, we can continue to refine our discount strategies and drive sustainable growth for our tech company.
