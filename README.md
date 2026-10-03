\# 💻 BUtech Laptop Finder



A smart laptop recommendation system built for \*\*BUtech\*\*, designed to help customers find laptops that match their software needs and budget.



The system combines a \*\*FastAPI backend\*\* with an interactive frontend to analyze customer requirements and recommend suitable laptops from the current BUtech inventory.



\---



\## ✨ Features



\* 🎯 Interactive laptop-finding wizard

\* 💰 Budget-based recommendations

\* 💻 Software-aware laptop matching

\* ⚡ CPU, GPU and RAM comparison

\* 📊 Match scores for recommended laptops

\* 💡 Explanations showing why each laptop was recommended

\* 🛒 Separate display for laptops within and above the customer's budget

\* 🖥️ Modern responsive customer interface

\* 🔧 Admin interface for managing laptop inventory

\* 📦 Current inventory contains 100 laptops



\---



\## 🧠 How It Works



The customer goes through a short questionnaire:



1\. \*\*Study / Major\*\*

2\. \*\*Laptop Usage\*\*

3\. \*\*Budget\*\*

4\. \*\*Required Software\*\*

5\. \*\*Personal Preferences\*\*



The selected software and budget are sent to the recommendation API.



The backend evaluates the available laptops and returns matching recommendations, including:



\* Match score

\* CPU

\* GPU

\* RAM

\* Price

\* Recommendation reasons



The customer then receives the most relevant laptops grouped into:



\* \*\*Within your budget\*\*

\* \*\*More powerful options\*\*



\---



\## 🏗️ Project Architecture



```text

BUtech-Laptop-Finder/

│

├── backend/

│   ├── main.py

│   ├── recommendation.py

│   └── prepare\_data.py

│

├── data/

│   └── laptops\_final.csv

│

├── frontend/

│   ├── admin/

│   │   ├── admin.html

│   │   ├── admin.css

│   │   └── admin.js

│   │

│   ├── assets/

│   │   └── hero-laptop.webp.jpg

│   │

│   ├── index.html

│   ├── script.js

│   └── style.css

│

└── .gitignore

```



\---



\## 🛠️ Tech Stack



\### Backend



\* Python

\* FastAPI

\* Uvicorn

\* Pandas



\### Frontend



\* HTML5

\* CSS3

\* JavaScript



\### Data \& Recommendation



\* CSV-based laptop inventory

\* Rule-based recommendation system

\* Software requirement matching



