# **Data Analyst Chatbot 🤖**

## **Description**

The **Data Analyst Chatbot** is an interactive application designed to assist users in performing demographic and statistical data analyses. Through an intuitive and user-friendly interface, users can ask natural language questions related to a specific dataset hosted in a PostgreSQL database. The chatbot interprets the questions, generates SQL queries using language models (OpenAI or AWS Bedrock), executes the queries, and returns detailed and concise responses.

---

## **Preprocessing**

Before uploading the data to the AWS PostgreSQL database, the dataset was preprocessed. This step ensures the data is consistent, easier to query, and relevant to the chatbot's functionality. Below are the preprocessing steps that were applied:

1. **Relevant Columns Selected**:
   Only the following columns were retained from the original dataset:

   - `REF_DATE`: Reference date of the record (Jan to Aug of 2017).
   - `TARGET`: Binary target for default (1 = Defaulter, i.e., overdue > 60 days in 2 months; 0 = Non-Defaulter).
   - `VAR2`: Gender of the individual.
   - `IDADE`: Age of the individual.
   - `VAR4`: Death flag (indicates whether the individual has passed away).
   - `VAR5`: Federative unit (state in Brazil).
   - `VAR8`: Estimated social class of the individual.

2. **Column Renaming**:
   The column names were renamed for consistency and better readability:

   - `REF_DATE` → `date`
   - `TARGET` → `defaulter`
   - `VAR2` → `sex`
   - `IDADE` → `age`
   - `VAR4` → `has_died`
   - `VAR5` → `uf`
   - `VAR8` → `social_class`

3. **Handling Missing Values**:

   - For the `has_died` column, any missing values were filled with `'N'` (indicating "No" for not deceased).

4. **Exporting the Cleaned Data**:
   The cleaned dataset was exported to a CSV file named `cleaned_neurotech_data.csv`.

5. **Purpose**:
   The cleaned data contains only the necessary information for the chatbot's operation, ensuring efficient querying and accurate responses.

---

The resulting dataset was then uploaded to the AWS PostgreSQL database, which serves as the backend data source for the chatbot.

---

## **Features**

- Generate SQL queries from natural language questions.
- Support for multiple language models:
  - **OpenAI GPT-4o mini**
  - **AWS Bedrock Llama 3.3 70B Instruct**
- Web interface developed with **Streamlit**.
- Organized and formatted responses for easier interpretation.
- Customizable configurations directly in the interface.

---

## **Installation**

### **Prerequisites**

- **Python** 3.9 or higher.
- **Poetry** for dependency management.
- **PostgreSQL** database configured and running.
- API keys:
  - OpenAI API.
  - AWS Access Key and Secret Access Key (if applicable).

### **Steps**

1. Clone this repository:

```bash
git clone https://github.com/your-username/data-analyst-chatbot.git
cd data-analyst-chatbot
```

2. Install the dependencies:

```bash
poetry install
```

3. Configure environment variables in the `.env` file:

```bash
DB_USER=your_postgres_user
DB_PASSWORD=your_postgres_password
DB_ENDPOINT=your_postgres_host
DB_PORT=5432
DB_NAME=your_database_name

OPENAI_API_KEY=your_openai_key
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
```

4. Start the backend with FastAPI:

```bash
poetry run uvicorn app.main:app --reload
```

5. Start the interface with Streamlit:

```bash
poetry run streamlit run interface/app.py
```

---

## **Usage**

### **Chatbot Configuration**

- Select the desired language model:
  - **GPT-4o mini** (OpenAI)
  - **Llama 3.3 70B Instruct** (AWS Bedrock).

### **Examples of Questions**

Here are some examples of questions you can ask the chatbot:

- "Qual estado tem a maior taxa de inadimplência?"
- "Qual é a porcentagem de mulheres que faleceram em cada estado?"
- "Qual é a idade média por estado?"
- "Quantas pessoas faleceram com mais de 50 anos?"

### **How It Works**

1. **Ask Your Question**: Enter a natural language question in the input field.
2. **Submit**: Click the "Send" button to process your question.
3. **Wait for Processing**: The backend will interpret your question, generate a SQL query, execute it on the database, and return the answer.
4. **View Results**: The response will be displayed in an intuitive and organized format.

### **Error Handling**

If there are any issues, such as incorrect queries or missing data:

- A descriptive error message will be displayed.
- Check the question for errors or consult the documentation for further guidance.

---

## Tests (WIP)

Tests have been implemented to validate the backend functionality and integration with language models. Only one test was implemented, in the future I will try to add more unit tests.

### Run Tests

Run the tests using pytest:

```bash
poetry run pytest
```

---

## Author

Developed by [Arthur Almeida](https://github.com/arthuraal).
