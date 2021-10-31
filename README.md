### Capstone - Developing a Recommendation System for Healthier Food Alternatives for Online Grocery Shopping
Team: Yiyan (James) Wan, Reshma Patil, Rameez Jafri

#### Problem statement
The United States Department of Health and Human Services recommends that consumers in the US need to improve their eating habits to meet recommended dietary guidelines. Frequently people choose poor nutrition quality products since the product labels offer difficult-to-understand and complex nutrition content of the product, and they lack information on better and healthier food alternatives at the point of purchase.      
Our research focuses on developing an online recommendation system to help customers’ select healthier food alternatives by providing them with targeted food recommendations based on overall measure of nutrition of food items. Consumers, online food retailers, and the government will all benefit from using this comprehensive nutrition measure.  The nutrition score provides consumers with an easy-to-understand score during their shopping experience, provides online food retailers with additional revenue from premium food sales, and improves the overall health of the populace.   
We develop a new and novel measure that computes the wholesome nutrient content of food items based on ingredients and processing methods. It incorporates methodologies suggested in academic literature in the field of health and nutrition. We use the nutrition score in comparing three data science methods based on machine learning models to recommend alternate healthier food options to people while shopping online, based on their shopping history, nutrition scores and prices of food items.


#### Analysis Goals
This project aims to create a tool that can help shift a consumer’s unhealthy eating habits to healthier ones. This may be achieved via targeted recommendations through an online grocery shopping platform. Using targeted recommendations may be helpful because the poor nutrition choices made by consumers can be the result of 1) difficulty understanding complex dietary or nutrition guidelines and 2) the lack of a system to monitor unhealthy shopping experiences while also recommending healthier food alternatives. These root causes for unhealthy eating can be addressed by the following: 1) assigning a straightforward nutrition score to each food item that represents its wholesome nutrient content based on ingredients and processing score, 2) applying customer segmentation to bucket similar customers for targeted recommendations, and finally 3) developing a recommendation system that provides healthier food options as alternatives based on customer similarity, shopping history, and nutrition score.

#### Data Sources
Grocery transaction and Category Dataset - 2017 Instacart Kaggle data (https://www.kaggle.com/c/instacart-market-basket-analysis/data)

Food Nutrition Database   - USDA, Nutritionix (Instacart), NutritionValue, Australian Food Standard Agency

#### Nutrition Scoring System

In order to provide consumers with a simple, easy to understand metric regarding the healthiness of each food item, we developed a nutrition score for over 58,000 food items which belong to 1,020 food sub-categories. We collected approximately 80 nutrients for individual food items. These nutrients are composed of both macro-nutrients and micro-nutrients. The nutrition content of each food item has been standardized to 100 grams or 100 milliliters. We studied the Environmental Working Group (EWG) score and Score of Nutritional Adequacy of Individual Foods (SAIN), the Nutrient to be Limited (LIM) further because both systems provided numerical bounds or formulae to calculate the nutritional score. These scores are widely used in the food industry to quantify nutrient value. We further modified these scores to make it suitable for our study;

1. Modified EWG Score - 
 - Calculated raw score
 - Flagged food contaminants
 - Penalized artificial additives
 - Nested ranking within a food category

2. Modified SAIN-LIM Score - 
 - Included 5 Positive Nutrients for SAIN score
 - Included 3 Negative Nutrients for LIM score
 - Added 17 positive nutrients
 - Added a negative nutrient
 - Combined SAIN and LIM Score

After analysis and comparison between modified SAIN – LIM and modified EWG, we have selected modified SAIN – LIM for our recommendation model due to wider consideration of nutrients and strong literature support. Also, with the type of data that we had, it suited SAIN-LIM scoring system much better as it did not require nutritional information related to food processing or food additives. Finally, the modified SAIN-LIM system was easily scalable to include more nutrients making it possible to calculate a single nutrient score and recommend alternatives to a broader set of food items. We could effectively scale this to more than 58,000+ food items in our database.

#### Modelling framework
1. Recommendation System:

* Model 1 (ECFAR) - 
This is a hybrid approach of the two main algorithms: association rule mining and collaborative filtering. Association Rule Mining (ARM) describes the relationships of purchases between different items, i.e., if product X is bought, then product Y is also bought. Collaborative filtering (CF) technique is widely used in ecommerce and it utilizes a set of ratings made by users on items to generate recommendations. This hybrid of approach is called the Extended algorithm based on Collaborative Filtering and Association Rule mining (ECFAR). The ECFAR covers two sub-algorithms. First, a parallel FP-Growth algorithm is used for mining association rules. Then, a parallel similar commodity discovery method based on matrix factorization is proposed, which implicitly implements the idea of CF. For CF matrix factorization we used Alternating Least Square (ALS) algorithm. We used big data platforms such as Spark when running ECFAR due to the large volume of transactions in the dataset. 

* Model 2 (USBC) - 
The second approach is user state binary classifier in which we predict previously purchased products will be in a customer’s next order, based on customers’ purchase history. In order to capture sequential behavior and general tastes of customers, we applied feature engineering to extract representative features from the customers historical purchase behavior. Meanwhile, we employed a neural network to model complicated interaction among customers and products. Although this approach could only recommend food items that users have purchased previouly, the result showed capability of generating accurate recommendation about products that a customer may want to purchase again.

* Model 3 (DREAM) -
In the third approach, we have captured sequential aspects of customers. The recommendation task in e-commerce sites is formulated as the next basket recommendation where we have a customer’s purchase data in a series of baskets of items at different time. To capture sequential features from historical transactions and the predict next purchase, Markov chain models has been successful. Although, more appropriate way to next basket recommendation is to capture sequential behavior and user general interest. For this purpose, we have used Dynamic Recurrent Basket Model (DREAM), based on Recurrent Neural Network (RNN). DREAM learns a dynamic representation of a user but also captures global sequential features among baskets.
    
2. Customer segmentation (To improve recommendation)

Based on our research over recommendation application in e-commerce industry, segmenting customers could improve the result of our recommendations. As such, we would like to incorporate this analysis on top of the recommendation to evaluate the effectiveness the customer segmentation. It is necessary to understand a customer’s shopping patterns and health consciousness which is possible through customer segmentation. Customers will be segmented based on two types of features: the customer’s previous shopping patterns and habits and the characteristics of the foods item they purchased, which includes prices and nutritions. In the future, additional features such as demographics and healthiness of the consumer can be added into the customer segmentation if the data becomes available. This information will allow us to know our customer better and deeper in terms of their spending power, shopping habits and nutrition needs. Based on the available features, two unsupervised clustering machine learning models were chosen: Gaussian Mixture Model (clustering technique for normally distributed features) and K-means clustering (a distance-based approached used for numerical features). These are two typical models that have been used in the industry based on our research. 

#### Evaluation Metric
Hit Ratio@15: % of items predicted correctly within top 15 in the next basket

Example: For a customer who purchased 20 items in their next basket, if model predicts 5 items correctly in top 15 predictions then the hit ratio is equal to 0.25 (5/20).

Hit Ratio Intervals: % of customers that fall into each Hit Ratio@15 interval

#### Results

* Quantitative comparison between 3 models:

| Hit Ratio Bucket |Model 1(ECFAR)|Model 2(USBC)|Model 3(DREAM)|
| -------------    |:-------------: | -----:    | -----:       |
| 0-0.2            | 30% | 25%    |         9%     |
| 0.2-0.4          | 27%      |   24%     |       21%       |
| 0.4-0.6          | 26%      |    20%     |      31%        |
| 0.6-0.8          | 9%      |    16%    |        21%    |
| 0.8-1.0          | 8%      |   15%    |          18%    |

DREAM was the winning model that had more customers falling into higher hit-ratio buckets such as 0.6-0.8 and 0.8-1.0.  For DREAM, we were able to predict more than 70% of the items correctly in the next basket for 40% of customer. 

* Customer Segmentation:
Regular and loyal customers have high frequency of purchasing through Instacart. They are also the ones that spent the most with the store. 
The circled three segments have a similar characteristic comparing to the health conscious is that they nutrition score/ price ratio are significantly lower. 
Those three segments accounted for 91% of the total population and we would like to direct those customers to a healthier shopping and eating style

![Customer Segmentation Interpretation](https://github.com/RAJ8430/Capstone-Project/blob/master/Result-Images/segments.PNG)

* Segment-level recommendation:
For the three targeted customer segments: regular, occasional, and loyal, we see a clear increase percentage for number of customers in the high hit ratio buckets and decrease in the low hit ratio buckets for both DREAM and USBC Models. In other words, customer segmentation improved the recommendation results to be more accurate and having more customers with more products predicted.    

By DREAM Model

![Segment Level Recommendation DREAM](https://github.com/RAJ8430/Capstone-Project/blob/master/Result-Images/segmentLevelRecommendation.PNG)

By USBC Model

![Segment Level Recommendation USBC](https://github.com/RAJ8430/Capstone-Project/blob/master/Result-Images/segmentLevelRecommendationUSBC.PNG)

#### Recommendation of Healthier Food Alternatives

After the recommendation system has offered recommendations to the customer and the customer has selected a product to place in the basket, the customer will also receive three additional recommendations on healthier alternatives. This recommendation is based on the nutrition to price ratio of the original product selected by the consumer. The three recommendations are as follows:

![Healthier Alternatives](https://github.com/RAJ8430/Capstone-Project/blob/master/Result-Images/HealthierAlternatives.PNG)

#### Project result summary

 - Consolidated a food database of 58K food items along with their nutrition and price using NLP framework
 - Developed a novel nutrition scoring system which considers 50+ nutrient types across 130+ food categories
 - Built a recommendation system which predicts more than 40% items accurately for 70% customers in their next purchase
 - Improved recommendation system by 4.5% through customer segmentation
 - Added a pipeline to the system that recommends healthier food alternatives


#### References
1.	 Wang P, Huang J, Cui Z, Xie L, Chen J. A Gaussian error correction multi-objective positioning Model with NSGA-II. Concurr Comput Pract Exp. 2019.In press. https://doi.org/10.1002/cpe.5464 
2.	Wang, Feiran & Wen, Yiping & Guo, Tianhang & Liu, Jianxun & Cao, Bu-Qing. (2019). Collaborative filtering and association rule mining‐based market basket recommendation on spark. Concurrency and Computation: Practice and Experience. 32. 10.1002/cpe.5565.
https://onlinelibrary.wiley.com/doi/full/10.1002/cpe.5565
3.	Yu, Feng & Liu, Qiang & Wu, Shu & Wang, Liang & Tan, Tieniu. (2016). A Dynamic Recurrent Model for Next Basket Recommendation. 729-732. 10.1145/2911451.2914683. https://dl.acm.org/doi/pdf/10.1145/2911451.2914683
4.	Darmon N, Vieux F, Maillot M, Volatier JL, Martin A. Nutrient profiles discriminate between foods according to their contribution to nutritionally adequate diets: a validation study using linear programming and the SAIN, LIM system. Am J Clin Nutr. 2009 Apr;89(4):1227-36. doi: 10.3945/ajcn.2008.26465. Epub 2009 Feb 11. PMID: 19211815.
5.	EWG’s Food Score: https://www.ewg.org/foodscores/
6.	Arambepola, Carukshi & Scarborough, Peter & Rayner, Mike. (2008). Validating a nutrient profile model. Public health nutrition. 11. 371-8. 10.1017/S1368980007000377.
https://www.ndph.ox.ac.uk/cpnp/publications/163685

#### Github Reference Repository
  - DREAM: https://github.com/RandolphVI/Next-Basket-Recommendation
  - USBC: https://github.com/graceofgod/Next-basket-recommendation-
