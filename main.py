# Load environment variables
from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import sqlite3
import google.generativeai as genai

# Configure Google Gemini API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini model and generate SQL query
def get_gemini_response(question, prompt):
    model = genai.GenerativeModel('gemini-pro')  # Correct model class name
    response = model.generate_content([prompt, question])  # Ensure both are strings
    return response.text.strip()  # Remove any extra spaces

# Function to execute SQL query on the SQLite database
def read_sql_query(sql, db):
    try:
        conn = sqlite3.connect(db)
        cur = conn.cursor()  # Fix: Added parentheses to `cursor()`
        cur.execute(sql)
        rows = cur.fetchall()
        conn.commit()
        conn.close()  # Fix: Added parentheses to close the connection
        return rows
    except Exception as e:
        return [f"Error: {str(e)}"]  # Return error message if SQL fails

# Define prompt as a string (not a list)
prompt = """
   You are an expert in converting English questions to SQL queries!
   The SQL database has the name STUDENT and has the following columns - NAME, CLASS, SECTION.

   Example 1:
   Question: How many entries of records are present?
   SQL: SELECT COUNT(*) FROM STUDENT;

   Example 2:
   Question: Tell me all the students studying in the Data Science class?
   SQL: SELECT * FROM STUDENT WHERE CLASS='Data Science';

   Ensure that the generated SQL does not contain ''' at the beginning and avoid the 'sql' keyword in the response.
"""

# Streamlit UI Setup
st.set_page_config(page_title="SQL Query Generator")  # Fix: Correct parameter name
st.header("🔍 AI-powered SQL Query Generator")

# Input field for user question
question = st.text_input("Enter your question:", key="input")

# Submit button
if st.button("Generate SQL Query"):
    if question:
        # Generate SQL query using Gemini AI
        sql_query = get_gemini_response(question, prompt)
        
        # Display the generated SQL query
        st.subheader("Generated SQL Query:")
        st.code(sql_query, language="sql")

        # Execute the SQL query on the SQLite database
        query_results = read_sql_query(sql_query, "student.db")

        # Display query results
        st.subheader("Query Results:")
        if query_results and "Error" not in query_results[0]:  # If no SQL error
            for row in query_results:
                st.write(row)  # Display each row from the database
        else:
            st.error(query_results[0])  # Show SQL error message
    else:
        st.warning("❗ Please enter a question before generating SQL.")
