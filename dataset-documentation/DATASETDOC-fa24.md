***Project Information*** 

* What is the project name?  
  * BU Hariri: Wheelock / BPS Policy Help Bot
* What is the link to your project’s GitHub repository? 
  * Link: https://github.com/BU-Spark/ml-bps-policy-bot 
* What is the link to your project’s Google Drive folder? \*\**This should be a Spark\! Owned Google Drive folder \- please contact your PM if you do not have access\*\**  
  * Link: https://drive.google.com/drive/u/1/folders/1mseCWp-9CYDDgeV8qY8qoM0IxdG0Xq--
* In your own words, what is this project about? What is the goal of this project? 
  * Our project aims to supports Boston Public Schools by simplifying access to English language public policy information through an intuitive RAG-based chatbot. Acting as a virtual assistant, the chatbot helps staff find policy-related answers and documents quickly, saving time on administrative tasks. By organizing policy documents into searchable pieces and using smart retrieval tools, it delivers accurate, clear responses through a user-friendly interface. With a focus on privacy and reliability, the chatbot enhances decision-making and streamlines navigating complex policies.  
* Who is the client for the project?
  * Boston Public School
* Who are the client contacts for the project?  
  * (Director of BPS - Michael Miller)
* What class was this project part of?
  * DS549

***Dataset Information***

* What data sets did you use in your project? Please provide a link to the data sets, this could be a link to a folder in your GitHub Repo, Spark\! owned Google Drive Folder for this project, or a path on the SCC, etc. 
  * Link: https://github.com/BU-Spark/ml-bps-policy-bot/tree/main/data/data_json/
* Please provide a link to any data dictionaries for the datasets in this project. If one does not exist, please create a data dictionary for the datasets used in this project. **(Example of data dictionary)**   
# Data Dictionary for JSON Dataset

This data dictionary describes the structure of the dataset used in the project. Each entry in the dataset corresponds to a chunk of a document stored in a Google Drive link.

## Fields

| **Field Name**  | **Description**                                                                                      | **Data Type** | **Example** |
|-----------------|------------------------------------------------------------------------------------------------------|---------------|-------------|
| `folder_name`   | The name of the folder containing the file.                                                           | String        | "Food and Nutrition Services" |
| `file_name`     | The name of the file that contains the content.                                                       | String        | "FNS-02 Emergency Meal Procedures" |
| `chunk_id`      | An identifier for the specific chunk or part of the document, indicating its order in the sequence.  | Integer       | 1           |
| `uri`           | A link to the file stored on Google Drive, providing access to the document.                         | String (URL)  | "https://drive.google.com/file/d/1VxLTLmK3rTa8BRrGablCSRJ_ClEDGxVI/view?usp=drive_link" |
| `content`       | The actual content or text from the document for the specific chunk.                                  | String        | "Page 1: Superintendent’s Circular NUMBER: FNS-02 Version 01 ..." |

## Key Insights:

- **`folder_name`**: Represents the broader category or directory the file belongs to (e.g., "Food and Nutrition Services").
- **`file_name`**: The specific name of the file, such as "FNS-02 Emergency Meal Procedures".
- **`chunk_id`**: A unique identifier used to break the document into smaller parts or chunks, which are likely sections of the full document.
- **`uri`**: The Google Drive link where the document can be accessed. It provides a direct URL to view or download the file.
- **`content`**: The content from that specific chunk of the document. This is often a snippet of a larger document, possibly a few pages or sections, presented as text.

## Usage:
This structure can be used across multiple entries in the dataset. Each entry will contain a set of chunks, each with its own `chunk_id`, `uri`, and `content`, corresponding to different sections of documents stored under various folders.

* What keywords or tags would you attach to the data set?  
  * **Keywords/Tags:**  
    NLP (Natural Language Processing)  
    RAG (Retrieval-Augmented Generation)  
    Chatbot  
    Policy Retrieval  
    Question Answering  
    Document-based Chatbot  
    Emergency Procedures NLP  
    Text Generation  
    Policy Interpretation  
    Knowledge Base  
    Information Retrieval  
    Text Summarization  
    Semantic Search  
    Policy Automation  
    Document Querying  
  * **Domain(s) of Application:**  
    NLP (specifically for building chatbots, question answering, and information retrieval systems)  
    Civic Tech (related to public policy and services)  
    Education (with a focus on school policies and emergency procedures)  

*The following questions pertain to the datasets you used in your project.*   
*Motivation* 

* For what purpose was the dataset created? Was there a specific task in mind? Was there a specific gap that needed to be filled? Please provide a description. 
  * The JSON file was created with the goal of providing enriched data to the FAISS vector database, enhancing retrieval and similarity search capabilities. We would continue to use this dataset for everything in our project, including EDA, summarization, tagging, and vector db.

*Composition*

* What do the instances that comprise the dataset represent (e.g., documents, photos, people, countries)? Are there multiple types of instances (e.g., movies, users, and ratings; people and interactions between them; nodes and edges)? What is the format of the instances (e.g., image data, text data, tabular data, audio data, video data, time series, graph data, geospatial data, multimodal (please specify), etc.)? Please provide a description.   
  * The instances consist of publicly accessible policy of Boston Public School.
* How many instances are there in total (of each type, if appropriate)?  
  * There are a total of 189 documents(instances).
* Does the dataset contain all possible instances or is it a sample (not necessarily random) of instances from a larger set? If the dataset is a sample, then what is the larger set? Is the sample representative of the larger set? If so, please describe how this representativeness was validated/verified. If it is not representative of the larger set, please describe why not (e.g., to cover a more diverse range of instances, because instances were withheld or unavailable).  
  * The dataset contains all the possible instances. It was cross-verified by the client.
* What data does each instance consist of? “Raw” data (e.g., unprocessed text or images) or features? In either case, please provide a description. 
  * It contains textual information only.  
* Is there any information missing from individual instances? If so, please provide a description, explaining why this information is missing (e.g., because it was unavailable). This does not include intentionally removed information, but might include redacted text.   
  * No information is missing.
* Are there recommended data splits (e.g., training, development/validation, testing)? If so, please provide a description of these splits, explaining the rationale behind them  
  * No data splits 
* Are there any errors, sources of noise, or redundancies in the dataset? If so, please provide a description.   
  * No erros, sources of noise, or redundancies in the dataset.
* Is the dataset self-contained, or does it link to or otherwise rely on external resources (e.g., websites, tweets, other datasets)? If it links to or relies on external resources,   
  * Are there guarantees that they will exist, and remain constant, over time;  
  * Are there official archival versions of the complete dataset (i.e., including the external resources as they existed at the time the dataset was created)?  
  * Are there any restrictions (e.g., licenses, fees) associated with any of the external resources that might apply to a dataset consumer? Please provide descriptions of all external resources and any restrictions associated with them, as well as links or other access points as appropriate.  
  * Answer: The dataset is locally stored on github branch.
* Does the dataset contain data that might be considered confidential (e.g., data that is protected by legal privilege or by doctor-patient confidentiality, data that includes the content of individuals’ non-public communications)? If so, please provide a description.   
  * No, we're working with publicly accessible data. 
* Does the dataset contain data that, if viewed directly, might be offensive, insulting, threatening, or might otherwise cause anxiety? If so, please describe why.   
  * No, there is no such data in out dataset.
* Is it possible to identify individuals (i.e., one or more natural persons), either directly or indirectly (i.e., in combination with other data) from the dataset? If so, please describe how.   
  * No, dataset contains policy documents.
* Dataset Snapshot, if there are multiple datasets please include multiple tables for each dataset. 


| Size of dataset |  |
| :---- | :---- |
| Number of instances | 189 |
| Number of fields  | N/A |
| Labeled classes |  N/A|
| Number of labels  |N/A |


  
*Collection Process*

* What mechanisms or procedures were used to collect the data (e.g., API, artificially generated, crowdsourced \- paid, crowdsourced \- volunteer, scraped or crawled, survey, forms, or polls, taken from other existing datasets, provided by the client, etc)? How were these mechanisms or procedures validated?  
  * The dataset is publicly accessible on the BPS website. We created a web scraper to scrape the links and then downloaded pdf text files from the drive links. We then stored our data in .txt file.
* If the dataset is a sample from a larger set, what was the sampling strategy (e.g., deterministic, probabilistic with specific sampling probabilities)?  
  * The dataset is not a sample of larger set.
* Over what timeframe was the data collected? Does this timeframe match the creation timeframe of the data associated with the instances (e.g., recent crawl of old news articles)? If not, please describe the timeframe in which the data associated with the instances was created. 
  * The dataset was created during Fall 2024 semester. The dataset itself contains files from Boston Public School policy website for the year of 2024/25.  
  Link: https://www.bostonpublicschools.org/domain/1884

*Preprocessing/cleaning/labeling* 

* Was any preprocessing/cleaning/labeling of the data done (e.g., discretization or bucketing, tokenization, part-of-speech tagging, SIFT feature extraction, removal of instances, processing of missing values)? If so, please provide a description. If not, you may skip the remaining questions in this section.   
  * Dataset was used raw.
* Were any transformations applied to the data (e.g., cleaning mismatched values, cleaning missing values, converting data types, data aggregation, dimensionality reduction, joining input sources, redaction or anonymization, etc.)? If so, please provide a description.   
  * No tranformations applied.
* Was the “raw” data saved in addition to the preprocessed/cleaned/labeled data (e.g., to support unanticipated future uses)? If so, please provide a link or other access point to the “raw” data, this could be a link to a folder in your GitHub Repo, Spark\! owned Google Drive Folder for this project, or a path on the SCC, etc.
  * N/A  
* Is the code that was used to preprocess/clean the data available? If so, please provide a link to it (e.g., EDA notebook/EDA script in the GitHub repository). 
  * The EDA was perfomed on dataset to understand it. However, raw data was used. No cleaning was perfomed on the dataset.

*Uses* 

* What tasks has the dataset been used for so far? Please provide a description.   
  * Dataset was used to create a RAG-based chatbot for Boston Public School to assist the affliated teachers and lawyers with BPS policy related question.
* What (other) tasks could the dataset be used for?
  * N/A  
* Is there anything about the composition of the dataset or the way it was collected and preprocessed/cleaned/labeled that might impact future uses? 
  * N/A  
* Are there tasks for which the dataset should not be used? If so, please provide a description.
  * N/A

*Distribution*

* Based on discussions with the client, what access type should this dataset be given (eg., Internal (Restricted), External Open Access, Other)?
  * Dataset is already publicly accessible.   
    Link: https://www.bostonpublicschools.org/domain/1884

*Maintenance* 

* If others want to extend/augment/build on/contribute to the dataset, is there a mechanism for them to do so? If so, please provide a description. 
  * We have code written to scrape the data, convert to text, and finally create metadata. All of it is available on github repository.

*Other*

* Is there any other additional information that you would like to provide that has not already been covered in other sections?
  * N/A

