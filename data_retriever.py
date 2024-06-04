import json
import os
import logging
import requests
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# 初始化词形还原器
lemmatizer = WordNetLemmatizer()

# 预处理函数
def preprocess_text(text):
    tokens  = re.split(r'[\s_]+', text)
    # 转为小写
    tokens = [token.lower() for token in tokens]
    # 去除停用词和词形还原
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalpha() and word not in stopwords.words('english')]
    return tokens

class SupplyChainDataRetriever:
    """
    A class to retrieve supply chain data from JSON files based on user queries.

    Attributes:
        database_folder (str): The path to the directory containing the JSON files.
        query_mapping (dict): A dictionary mapping query keywords to JSON file names.

    Methods:
        get_supply_chain_data(query): Retrieves supply chain data based on the user's query.
    """

    def __init__(self, database_folder, mapping_api_url='http://localhost:5001/mapping'):
        """
        Initializes the SupplyChainDataRetriever instance.

        Args:
            database_folder (str): The path to the directory containing the JSON files.
        """
        self.database_folder = database_folder
        self.query_mapping = self.fetch_query_mapping(mapping_api_url)

    def fetch_query_mapping(self, mapping_api_url):
        try:
            response = requests.get(mapping_api_url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching query_mapping: {e}")
            return {}
        logger.info(f"SupplyChainDataRetriever instance created with database folder: {database_folder}")

    def get_supply_chain_data(self, query):
        """
        Retrieves supply chain data based on the user's query.

        Args:
            query (str): The user's query related to a supply chain activity.

        Returns:
            dict: The corresponding supply chain data if the query matches a known activity, or an error message.
        """
        query = query.lower()
        logger.info(f"Received query: {query}")

        # Check if the query matches any of the known supply chain activities
        for activity, filename in self.query_mapping.items():
            # 文本预处理
            activity_words = preprocess_text(activity)
            query_words = preprocess_text(query)

            # 打印预处理后的单词
            print(f"activity_words = {activity_words}")
            print(f"query_words = {query_words}")

            # 特征提取：使用TF-IDF
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform([' '.join(activity_words), ' '.join(query_words)])

            # 计算余弦相似度
            similarity_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

            print(f"Text Similarity Score: {similarity_score[0][0]}")

            if similarity_score[0][0] >= 0.3:
                file_path = os.path.join(self.database_folder, filename)
                if os.path.exists(file_path):
                    logger.info(f"Reading data from file: {file_path}")
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                    logger.info(f"Retrieved data: {data}")
                    return data
                else:
                    logger.error(f"File not found: {file_path}")

        # If no matching activity is found, return an error message
        error_message = {"error": "No data found for the given query"}
        logger.warning(f"No data found for query: {query}")
        return error_message