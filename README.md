# 🧠 AI SmartQuizzer Pro

AI SmartQuizzer Pro is an intelligent quiz generator built with **Python** and **Streamlit**. It allows users to generate quizzes automatically from a PDF, TXT file, or a topic input. The app evaluates answers, tracks time, and generates a detailed PDF report of the quiz performance.

---

## 🛠 Features

- **AI-powered quiz generation:** Generate multiple-choice quizzes from PDF files, text files, or topic keywords.  
- **Dynamic options:** Automatically creates distractors for multiple-choice questions.  
- **Timed quizzes:** Customizable timer for quizzes.  
- **Interactive quiz interface:** Previous, Next, and Submit buttons for seamless navigation.  
- **Real-time score evaluation:** Get your score as you submit the quiz.  
- **PDF report download:** Generate a professional quiz report with correct answers and explanations.  
- **User-friendly UI:** Built with Streamlit with responsive cards, timer, and buttons.  

---

## 🧩 Installation

```bash
1️⃣ Clone the repository
git clone https://github.com/Ankita-Kumari0309/AI_SmartQuizzer.git
cd AI_SmartQuizzer

2️⃣ Create a virtual environment
python -m venv env

3️⃣ Activate the virtual environment
Windows PowerShell
.\env\Scripts\Activate.ps1

Windows CMD
env\Scripts\activate.bat
Mac / Linux
source env/bin/activate

4️⃣ Install dependencies
pip install -r requirements.txt

5️⃣ Run the app
streamlit run app.py

```
## 📊 Output

1. Quiz Generation Screen:
Users can upload a PDF/TXT file or enter a topic to instantly generate AI-powered multiple-choice questions.

2. Interactive Quiz Interface:
Displays one question at a time with Previous, Next, and Submit buttons, along with a real-time countdown timer.

3. Live Score Evaluation:
After submission, the system instantly calculates the final score, highlights correct and incorrect answers, and shows explanations.

4. Detailed PDF Report:
Users can download a professional PDF report containing:

-- Total score

-- Correct answers

-- Selected answers

-- Answer explanations

5. User-Friendly Dashboard:
A clean and responsive Streamlit UI with cards, buttons, and progress indicators for a smooth user experience.

<img width="1917" height="1079" alt="Screenshot 2026-01-09 201526" src="https://github.com/user-attachments/assets/b146e005-213f-4e89-8908-1fb1c0305b9e" />

<img width="1919" height="968" alt="Screenshot 2026-01-09 201623" src="https://github.com/user-attachments/assets/88c9ac6d-df4c-4952-b940-09deea2d20fa" />




## 🧰 Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **AI / NLP:** LLM-based question generation  
- **File Handling:** PDF & TXT parsing  
- **Reporting:** PDF generation  
- **Libraries:** LangChain, PyPDF2, FPDF, Streamlit

## 📂 Project Structure

<img width="279" height="190" alt="image" src="https://github.com/user-attachments/assets/9fd579b0-3154-4b9f-be39-17c6ee8abbdb" />


## 🔄 How It Works

1. User uploads a PDF/TXT file or enters a topic  
2. Text is extracted and preprocessed  
3. AI model generates questions and options  
4. User attempts the timed quiz  
5. System evaluates answers  
6. A detailed PDF report is generated

## 🎯 Use Cases

- Online learning platforms  
- Student self-assessment  
- Interview preparation  
- Corporate training & evaluation  
- Faculty quiz creation

  ## 🔮 Future Enhancements

- User login and quiz history  
- Difficulty-level based questions  
- Support for more file formats  
- Voice-based quiz interaction  
- Leaderboard and analytics dashboard
