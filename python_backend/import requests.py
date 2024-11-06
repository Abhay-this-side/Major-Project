import csv
import re
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm  # Progress bar library

# Define topic keywords
topic_keywords = {
    "Data Science": ["data science", "machine learning", "deep learning", "ai", "analytics"],
    "Python": ["python"],
    "Java": ["java"],
    "SQL": ["sql", "database", "mysql", "mongodb", "postgresql", "pl/sql"],
    "JavaScript": ["javascript", "jquery", "nodejs", "react", "angular", "vuejs"],
    "DevOps": ["devops", "docker", "kubernetes", "jenkins", "ansible", "git", "ci/cd", "powershell"],
    "Cloud Computing": ["aws", "azure", "google cloud", "cloud computing", "cloud engineer"],
    "Web Development": ["html", "css", "web development", "frontend", "backend", "web api", "web services"],
    "Mobile Development": ["android", "ios", "react native", "flutter", "mobile development"],
    "Cybersecurity": ["cybersecurity", "ethical hacking", "information security"],
    "Data Engineering": ["data engineer", "big data", "spark", "hadoop", "etl", "data pipeline", "kafka"],
    "Software Engineering": ["software engineering", "system design", "low-level design", "oop"],
    "Testing": ["selenium", "appium", "automation testing", "qa", "sdet", "testing"],
    "Digital Marketing": ["digital marketing", "seo", "content marketing", "ppc", "social media"],
    "Behavioral": ["behavioral interview", "soft skills", "communication"],
    "Project Management": ["project management", "agile", "scrum", "jira", "pmp"],
    "Mathematics and Statistics": ["linear regression", "probability", "statistics", "quantitative"],
    "Miscellaneous": ["excel", "tableau", "matlab", "iot", "technical support", "system administration"],
}

# List of URLs
urls = [
    "https://www.simplilearn.com/tutorials/data-science-tutorial/data-science-interview-questions",
    "https://www.simplilearn.com/tutorials/python-tutorial/python-interview-questions",
    "https://www.simplilearn.com/tutorials/java-tutorial/java-interview-questions",
    "https://www.simplilearn.com/tutorials/nodejs-tutorial/nodejs-interview-questions",
    "https://www.simplilearn.com/tutorials/javascript-tutorial/jquery-interview-questions",
    "https://www.simplilearn.com/tutorials/data-analytics-tutorial/data-analyst-interview-questions",
    "https://www.simplilearn.com/tutorials/cpp-tutorial/cpp-interview-questions",
    "https://www.simplilearn.com/coding-interview-questions-article",
    "https://www.simplilearn.com/top-api-testing-interview-questions-article",
    "https://www.simplilearn.com/tutorials/digital-marketing-tutorial/digital-marketing-interview-questions",
    "https://www.simplilearn.com/tutorials/agile-scrum-tutorial/scrum-master-interview-questions",
    "https://www.simplilearn.com/tutorials/reactjs-tutorial/reactjs-interview-questions",
    "https://www.simplilearn.com/tutorials/angular-tutorial/angular-interview-questions",
    "https://www.interviewbit.com/react-interview-questions/",
    "https://www.interviewbit.com/sql-interview-questions/",
    "https://www.interviewbit.com/oops-interview-questions/",
    "https://www.interviewbit.com/css-interview-questions/",
    "https://www.interviewbit.com/django-interview-questions/",
    "https://www.interviewbit.com/networking-interview-questions/",
    "https://www.interviewbit.com/javascript-interview-questions/",
    "https://www.interviewbit.com/jquery-interview-questions/",
    "https://www.interviewbit.com/angular-interview-questions/",
    "https://www.interviewbit.com/data-structure-interview-questions/",
    "https://www.interviewbit.com/c-interview-questions/",
    "https://www.interviewbit.com/php-interview-questions/",
    "https://www.interviewbit.com/c-sharp-interview-questions/",
    "https://www.interviewbit.com/web-api-interview-questions/",
    "https://www.interviewbit.com/hibernate-interview-questions/",
    "https://www.interviewbit.com/node-js-interview-questions/",
    "https://www.interviewbit.com/cpp-interview-questions/",
    "https://www.interviewbit.com/oops-interview-questions/",
    "https://www.interviewbit.com/devops-interview-questions/",
    "https://www.interviewbit.com/machine-learning-interview-questions/",
    "https://www.interviewbit.com/docker-interview-questions/",
    "https://www.interviewbit.com/mysql-interview-questions/",
    "https://www.interviewbit.com/css-interview-questions/",
    "https://www.interviewbit.com/laravel-interview-questions/",
    "https://www.interviewbit.com/asp-net-interview-questions/",
    "https://www.interviewbit.com/django-interview-questions/",
    "https://www.interviewbit.com/dot-net-interview-questions/",
    "https://www.interviewbit.com/kubernetes-interview-questions/",
    "https://www.interviewbit.com/operating-system-interview-questions/",
    "https://www.interviewbit.com/react-native-interview-questions/",
    "https://www.interviewbit.com/aws-interview-questions/",
    "https://www.interviewbit.com/git-interview-questions/",
    "https://www.interviewbit.com/java-8-interview-questions/",
    "https://www.interviewbit.com/mongodb-interview-questions/",
    "https://www.interviewbit.com/dbms-interview-questions/",
    "https://www.interviewbit.com/spring-boot-interview-questions/",
    "https://www.interviewbit.com/power-bi-interview-questions/",
    "https://www.interviewbit.com/pl-sql-interview-questions/",
    "https://www.interviewbit.com/tableau-interview-questions/",
    "https://www.interviewbit.com/linux-interview-questions/",
    "https://www.interviewbit.com/ansible-interview-questions/",
    "https://www.interviewbit.com/java-interview-questions/",
    "https://www.interviewbit.com/jenkins-interview-questions/",
    "https://www.interviewbit.com/agile-interview-questions/",
    "https://www.interviewbit.com/networking-interview-questions/",
    "https://www.interviewbit.com/azure-interview-questions/",
    "https://www.interviewbit.com/automation-testing-interview-questions/",
    "https://www.interviewbit.com/android-interview-questions/",
    "https://www.interviewbit.com/hr-interview-questions/",
    "https://www.interviewbit.com/rest-api-interview-questions/",
    "https://www.interviewbit.com/unix-interview-questions/",
    "https://www.interviewbit.com/multithreading-interview-questions/",
    "https://www.interviewbit.com/typescript-interview-questions/",
    "https://www.interviewbit.com/angular-8-interview-questions/",
    "https://www.interviewbit.com/salesforce-interview-questions/",
    "https://www.interviewbit.com/spark-interview-questions/",
    "https://www.interviewbit.com/bootstrap-interview-questions/",
    "https://www.interviewbit.com/web-services-interview-questions/",
    "https://www.interviewbit.com/jsp-interview-questions/",
    "https://www.interviewbit.com/html-interview-questions/",
    "https://www.interviewbit.com/hadoop-interview-questions/",
    "https://www.interviewbit.com/angularjs-interview-questions/",
    "https://www.interviewbit.com/cucumber-interview-questions/",
    "https://www.interviewbit.com/cyber-security-interview-questions/",
    "https://www.interviewbit.com/jdbc-interview-questions/",
    "https://www.interviewbit.com/microservices-interview-questions/",
    "https://www.interviewbit.com/ccna-interview-questions/",
    "https://www.interviewbit.com/data-science-interview-questions/",
    "https://www.interviewbit.com/cloud-computing-interview-questions/",
    "https://www.interviewbit.com/spring-interview-questions/",
    "https://www.interviewbit.com/scrum-master-interview-questions/",
    "https://www.interviewbit.com/big-data-interview-questions/",
    "https://www.interviewbit.com/wcf-interview-questions/",
    "https://www.interviewbit.com/data-analyst-interview-questions/",
    "https://www.interviewbit.com/maven-interview-questions/",
    "https://www.interviewbit.com/linked-list-interview-questions/",
    "https://www.interviewbit.com/sql-interview-questions/",
    "https://www.interviewbit.com/ssis-interview-questions/",
    "https://www.interviewbit.com/kafka-interview-questions/",
    "https://www.interviewbit.com/vmware-interview-questions/",
    "https://www.interviewbit.com/kotlin-interview-questions/",
    "https://www.interviewbit.com/deep-learning-interview-questions/",
    "https://www.interviewbit.com/postman-interview-questions/",
    "https://www.interviewbit.com/appium-interview-questions/",
    "https://www.interviewbit.com/iot-interview-questions/",
    "https://www.interviewbit.com/database-testing-interview-questions/",
    "https://www.interviewbit.com/ios-interview-questions/",
    "https://www.interviewbit.com/jira-interview-questions/",
    "https://www.interviewbit.com/redux-interview-questions/",
    "https://www.interviewbit.com/spring-security-interview-questions/",
    "https://www.interviewbit.com/golang-interview-questions/",
    "https://www.interviewbit.com/qa-interview-questions/",
    "https://www.interviewbit.com/nlp-interview-questions/",
    "https://www.interviewbit.com/react-interview-questions/",
    "https://www.interviewbit.com/sdet-interview-questions/",
    "https://www.interviewbit.com/powershell-interview-questions/",
    "https://www.interviewbit.com/data-modelling-interview-questions/",
    "https://www.interviewbit.com/system-design-interview-questions/",
    "https://www.interviewbit.com/web-developer-interview-questions/",
    "https://www.interviewbit.com/technical-support-interview-questions/",
    "https://www.interviewbit.com/full-stack-developer-interview-questions/",
    "https://www.interviewbit.com/front-end-developer-interview-questions/",
    "https://www.interviewbit.com/software-engineering-interview-questions/",
    "https://www.interviewbit.com/data-engineer-interview-questions/",
    "https://www.interviewbit.com/low-level-design-interview-questions/",
    "https://www.interviewbit.com/hashmap-interview-questions/",
    "https://www.interviewbit.com/java-programming-interview-questions/",
    "https://www.interviewbit.com/wordpress-interview-questions/",
    "https://www.interviewbit.com/sql-joins-interview-questions/",
    "https://www.interviewbit.com/computer-science-interview-questions/",
    "https://www.interviewbit.com/ci-cd-interview-questions/",
    "https://www.interviewbit.com/selenium-interview-questions/",
    "https://www.interviewbit.com/linear-regression-interview-questions/",
    "https://www.interviewbit.com/vue-js-interview-questions/",
    "https://www.interviewbit.com/behavioral-interview-questions/",
    "https://www.interviewbit.com/exception-handling-interview-questions/",
    "https://www.interviewbit.com/matlab-interview-questions/",
    "https://www.interviewbit.com/excel-interview-questions/",
    "https://www.interviewbit.com/aws-lambda-interview-questions/",
    "https://www.interviewbit.com/probability-interview-questions/",
]

def identify_topic(question):
    """Identify topic based on keywords in the question."""
    for topic, keywords in topic_keywords.items():
        if any(keyword.lower() in question.lower() for keyword in keywords):
            return topic
    return "General"  # Default if no keywords match

def remove_serial_number(question):
    """Remove any leading serial number (e.g., '15. ') from a question."""
    return re.sub(r"^\d+\.\s*", "", question)

def scrape_interview_questions():
    """Scrape questions, filter by serial number, clean, identify topics, and write to CSV with progress tracking."""
    all_questions = []
    
    for url in tqdm(urls, desc="Scraping progress"):
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract question text based on website structure (e.g., using <h3> tags)
            questions = soup.find_all('h3')  # Adjust if needed based on actual HTML structure
            
            for question in questions:
                text = question.get_text(strip=True)
                
                # Only include questions with a leading serial number
                if re.match(r"^\d+\.\s", text):
                    clean_text = remove_serial_number(text)
                    topic = identify_topic(clean_text)
                    all_questions.append([clean_text, topic])
        
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve data from {url}: {e}")

    # Write questions to CSV file
    with open('interview_questions.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Question', 'Topic'])
        writer.writerows(all_questions)

    print(f"Scraping completed. {len(all_questions)} questions saved to 'interview_questions.csv'.")

# Run the scraping function
scrape_interview_questions()