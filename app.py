import streamlit as st
import pandas as pd
from collections import defaultdict
import time
from datetime import datetime, timedelta

# from streamlit_confetti import st_confetti
from streamlit_confetti import confetti

# Set page config
st.set_page_config(page_title="MCQ Practice App", 
                   layout="wide", 
                   initial_sidebar_state="expanded",
                   page_icon="📚"
                   )

# Custom CSS for better styling
def load_css():
    st.markdown("""
        <style>
        .stRadio > label {
            background-color: #f0f2f6;
            padding: 10px;
            border-radius: 5px;
            width: 100%;
            margin: 10px 0;
            transition: background-color 0.3s;
        }
        .stRadio > label:hover {
            background-color: #e0e2e6;
        }
        .question-card {
            # background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin: 20px 0;
        }
        .timer-widget {
            background-color: #ff4b4b;
            color: white;
            padding: 10px;
            border-radius: 5px;
            text-align: center;
            font-size: 20px;
            margin: 10px 0;
        }
        .score-card {
            background-color: #4CAF50;
            color: white;
            padding: 1px;
            border-radius: 10px;
            text-align: center;
            margin: 20px 0;
        }
        .correct-answer {
            color: #4CAF50;
            font-weight: bold;
        }
        .wrong-answer {
            color: #ff4b4b;
            font-weight: bold;
        }
        .navigation-btn {
            background-color: #1f77b4;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
        }
        .credits {
            text-align: center;
            padding: 10px;
            # background-color: #f8f9fa;
            border-radius: 5px;
            margin: 20px 0;
        }
        .credits a {
            color: #1f77b4;
            text-decoration: none;
        }
        .credits a:hover {
            text-decoration: underline;
        }
        .submit-button {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 1000;
        }
        
        </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = defaultdict(str)
    if 'show_results' not in st.session_state:
        st.session_state.show_results = False
    if 'start_time' not in st.session_state:
        st.session_state.start_time = datetime.now()
    if 'time_remaining' not in st.session_state:
        st.session_state.time_remaining = timedelta(minutes=15)

def display_timer():
    current_time = datetime.now()
    elapsed_time = current_time - st.session_state.start_time
    remaining_time = st.session_state.time_remaining - elapsed_time

    if remaining_time.total_seconds() <= 0:
        st.session_state.show_results = True
        st.rerun()

    minutes = int(remaining_time.total_seconds() // 60)
    seconds = int(remaining_time.total_seconds() % 60)
    st.markdown(f"""
        <div class="timer-widget">
            Time Remaining: {minutes:02d}:{seconds:02d}
        </div>
    """, unsafe_allow_html=True)

def display_question(question, index):
    st.markdown(f"""
        <div class="question-card">
            <h3>{question['question']}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    selected_option = st.radio(
        "Select your answer:",
        question['options'],
        key=f"q_{index}",
        index=None,
        label_visibility="collapsed"
    )
    
    if selected_option:
        st.session_state.user_answers[index] = selected_option[0]

def display_results(questions, results, correct, total):
    st.markdown(f"""
        <div class="score-card">
            <h2>Quiz Complete!</h2>
            <h3>Your Score: {correct}/{total} ({(correct/total*100):.1f}%)</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Performance summary
    performance_data = {
        'Correct Answers': correct,
        'Wrong Answers': total - correct,
        'Accuracy': f"{(correct/total*100):.1f}%"
    }
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Performance Summary")
        for key, value in performance_data.items():
            st.markdown(f"**{key}:** {value}")
    
    # Detailed Review
    st.markdown("### Question Review")
    for result in results:
        with st.expander(result['question']):
            if result['is_correct']:
                st.markdown(f"""
                    <div style='color: #4CAF50;'>
                        ✓ Correct! You selected: {result['user_answer']}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div style='color: #ff4b4b;'>
                        ✗ Wrong! You selected: {result['user_answer']}
                    </div>
                    <div style='color: #4CAF50;'>
                        Correct answer: {result['correct_answer']}
                    </div>
                """, unsafe_allow_html=True)

def main():
    load_css()
    
    # Header with credits
    st.markdown("""
        <h1 style='text-align: center; color: #1f77b4;'>ABE501 MCQ Practice</h1>
        <h3 style='text-align: center; color: #666;'>Management Engineering Exam Preparation</h3>
        <div class='credits'>
            Built with ❤️ by <a href='https://github.com/Abdulraqib20' target='_blank'>raqibcodes</a>
        </div>
    """, unsafe_allow_html=True)
    
    initialize_session_state()
    
    #################################################################################################################
    ################################### QUESTIONS ################################################################
    # Add your questions list here
    questions = [
        {
            "question": "1. First-line managers are responsible for what?",
            "options": [
                "A. Managing non-managers",
                "B. Managing through other managers",
                "C. Setting long-term plans",
                "D. None of the above"
            ],
            "correct_answer": "A"
        },
        {
            "question": "2. Which of the following best describes interpersonal roles and decision roles?",
            "options": [
                "A. They involve interactions with people inside and outside the organization",
                "B. They focus only on making financial decisions",
                "C. They do not require communication skills",
                "D. They are unrelated to managerial positions"
            ],
            "correct_answer": "A"
        },
        {
            "question": "3. What is the ratio of output to material input?",
            "options": [
                "A. Labour productivity",
                "B. Financial productivity",
                "C. Material productivity",
                "D. None of the above"
            ],
            "correct_answer": "C"
        },
        {
            "question": "4. An engineer is known as ___ if less effort is used to achieve the same value of output.",
            "options": [
                "A. Effective",
                "B. Efficient",
                "C. None of the above",
                "D. Effascent"
            ],
            "correct_answer": "B"
        },
        {
            "question": "5. Which of the following isn’t among the Forecasting Procedure?",
            "options": [
                "A. Statement of the problem",
                "B. Definition of the scope (short or long term)",
                "C. Setting of objectives",
                "D. Cross-checking values to ensure consistency"
            ],
            "correct_answer": "D"
        },
        {
            "question": "6. A plan designed to coordinate a large set of activities is called:",
            "options": [
                "A. Project",
                "B. Budget",
                "C. Program",
                "D. Financial Statement"
            ],
            "correct_answer": "C"
        },
        {
            "question": "7. The most important skill of a project manager is:",
            "options": [
                "A. Leadership",
                "B. Technical expertise",
                "C. Financial management",
                "D. Communication"
            ],
            "correct_answer": "A"
        },
        {
            "question": "8. Which of these is not among types of leaders?",
            "options": [
                "A. Keep it simple style",
                "B. Lion-hearted leader",
                "C. Historically minded leader",
                "D. None of the above"
            ],
            "correct_answer": "D"
        },
        {
            "question": "9. Which of the following best describes a top-level manager?",
            "options": [
                "A. Director",
                "B. Executive director",
                "C. Manager",
                "D. All of the above"
            ],
            "correct_answer": "D"
        },
        {
            "question": "10. ____ are plans that describe the exact series of actions to be taken.",
            "options": [
                "A. Procedure",
                "B. Strategy",
                "C. Rules",
                "D. Goals"
            ],
            "correct_answer": "A"
        },
        {
            "question": "11. A plan designed to coordinate a large set of activities is called a:",
            "options": [
                "A. Program",
                "B. Budget",
                "C. Project",
                "D. Framework"
            ],
            "correct_answer": "A"
        },
        {
            "question": "12. The function of management concerned with monitoring and adjusting performance is:",
            "options": [
                "A. Controlling",
                "B. Planning",
                "C. Organizing",
                "D. Leading"
            ],
            "correct_answer": "A"
        },
        {
            "question": "13. What is the third step in the controlling cycle?",
            "options": [
                "A. Top managers set standards",
                "B. Performance is analyzed through qualitative and quantitative measures",
                "C. Performance is compared with set standards",
                "D. If performance exceeds set standards, no creative work is done"
            ],
            "correct_answer": "C"
        },
        {
            "question": "14. Ways to avoid organizational inflexibility are as follows except:",
            "options": [
                "A. Avoid inflexibility through organization",
                "B. Avoid flexibility",
                "C. Need for readjustment and change",
                "D. None of the above"
            ],
            "correct_answer": "B"
        },
        {
            "question": "15. Forecasting procedure includes the following except:",
            "options": [
                "A. Definition of scope",
                "B. Setting of objectives",
                "C. Cross-checking values",
                "D. None"
            ],
            "correct_answer": "D"
        },
        {
            "question": "16. A good forecast should have the following characteristics:",
            "options": [
                "A. It must produce fairly accurate results",
                "B. It must be simple to use",
                "C. It must be cost-conscious",
                "D. All of the above"
            ],
            "correct_answer": "D"
        },
        {
            "question": "17. What is the most essential attribute of a project manager?",
            "options": [
                "A. Leadership",
                "B. Charisma",
                "C. Communication skill",
                "D. Technical expertise"
            ],
            "correct_answer": "A"
        },
        {
            "question": "18. What refers to establishing interrelationships between people and things in such a way that human and material resources are effectively focused toward achieving the company’s goal?",
            "options": [
                "A. Planning",
                "B. Leading",
                "C. Controlling",
                "D. Organizing"
            ],
            "correct_answer": "D"
        },
        {
            "question": "19. What refers to the collection of tools and techniques that are used on a predefined set of inputs to produce a predefined set of outputs?",
            "options": [
                "A. Project Management",
                "B. Engineering Management",
                "C. Management",
                "D. Planning"
            ],
            "correct_answer": "A"
        },
        {
            "question": "20. Which manager is responsible for planning, pricing, and promoting products and making them available to customers?",
            "options": [
                "A. Sales Manager",
                "B. Product Manager",
                "C. Marketing Manager",
                "D. Business Development Manager"
            ],
            "correct_answer": "C"
        },
        {
            "question": "21. What type of management is responsible for First-Line Management?",
            "options": [
                "A. Supervising workers",
                "B. Overseeing daily operations",
                "C. Directing and controlling primary functions",
                "D. All of the above"
            ],
            "correct_answer": "D"
        },
        {
            "question": "22. Creating a viable organization involves:",
            "options": [
                "A. Avoiding mistakes in organizing by planning",
                "B. Avoiding organizational inflexibility",
                "C. Making staff work effective",
                "D. All of the above"
            ],
            "correct_answer": "D"
        },
        {
            "question": "23. Forecasting method helps in the following except:",
            "options": [
                "A. Produce product in fairly accurate",
                "B. Cost-conscious",
                "C. Simple to use",
                "D. All of the above"
            ],
            "correct_answer": "D"
        },
        {
            "question": "24. A manager does the following functions except:",
            "options": [
                "A. Leading",
                "B. Directing",
                "C. Measuring",
                "D. Controlling"
            ],
            "correct_answer": "C"
        },
        {
            "question": "25. Engineers can become good managers only through:",
            "options": [
                "A. Experience",
                "B. Taking a master's degree in management",
                "C. Effective career planning",
                "D. Training"
            ],
            "correct_answer": "C"
        },
        {
            "question": "26. Managers within the field of engineering are trained to understand:",
            "options": [
                "A. Human resource management",
                "B. Finances",
                "C. Industrial psychology",
                "D. All of the above"
            ],
            "correct_answer": "D"
        },
        {
            "question": "27. Which of these is not among the types of leaders?",
            "options": [
                "A. Keep it simple style",
                "B. Lion-hearted leader",
                "C. Historically minded leader",
                "D. Silent type"
            ],
            "correct_answer": "D"
        },
        {
            "question": "28. ______ is the work done or performance to increase the value of a company.",
            "options": [
                "A. Power",
                "B. Energy",
                "C. Overtime",
                "D. Works"
            ],
            "correct_answer": "D"
        },
        {
            "question": "29. Top managers' functions include:",
            "options": [
                "A. Setting organizational goals",
                "B. Making major decisions",
                "C. Overseeing company policies",
                "D. All of the above"
            ],
            "correct_answer": "D"
        },
        {
            "question": "30. The Board of Executives does which of the following?",
            "options": [
                "A. Recruit, monitor, and fire managers and top executives",
                "B. Develop marketing strategies",
                "C. Handle day-to-day operations",
                "D. Supervise production processes"
            ],
            "correct_answer": "A"
        },
        {
            "question": "31. What does a First-Line Manager do?",
            "options": [
                "A. Supervise all other workers",
                "B. Manage through other managers",
                "C. Develop long-term strategies",
                "D. Set organizational policies"
            ],
            "correct_answer": "A"
        },
        {
            "question": "32. The definition of management includes:",
            "options": [
                "A. What a manager does",
                "B. The art and science of decision-making and planning",
                "C. The process of achieving goals through people",
                "D. All of the above"
            ],
            "correct_answer": "D"
        },
        {
            "question": "33. The third step in the cycle of controlling is:",
            "options": [
                "A. Setting standards",
                "B. Measuring performance",
                "C. Comparing the result with the established standard and seeing the difference",
                "D. Taking corrective actions"
            ],
            "correct_answer": "C"
        },
        {
            "question": "34. Organizing in management refers to:",
            "options": [
                "A. Assigning tasks and responsibilities",
                "B. Coordinating resources efficiently",
                "C. Structuring work relationships",
                "D. All of the above"
            ],
            "correct_answer": "D"
        },
        {
            "question": "35. Planning in management involves:",
            "options": [
                "A. Setting objectives",
                "B. Determining courses of action",
                "C. Allocating resources",
                "D. All of the above"
            ],
            "correct_answer": "D"
        },
        {
            "question": "36. The role of a marketing manager includes:",
            "options": [
                "A. Developing marketing strategies",
                "B. Managing customer relationships",
                "C. Overseeing promotional campaigns",
                "D. All of the above"
            ],
            "correct_answer": "D"
        },
        {
            "question": "37. Staffing in management refers to:",
            "options": [
                "A. Recruiting and selecting employees",
                "B. Training and developing employees",
                "C. Retaining and motivating employees",
                "D. All of the above"
            ],
            "correct_answer": "D"
        },
        {
            "question": "38. The definition of management includes:",
            "options": [
                "A. Management is the art and science of decision-making and leadership",
                "B. Management is what a manager does",
                "C. All of the above",
                "D. Initiation and maintenance of an investment portfolio"
            ],
            "correct_answer": "C"
        }
    ]
        #################################################################################################################
        #################################################################################################################
        
    
    if not questions:
        st.warning("Please add your questions to the questions list!")
        return
    
    # Display timer
    if not st.session_state.show_results:
        display_timer()
    
    # Questions per page
    questions_per_page = 5
    total_pages = (len(questions) + questions_per_page - 1) // questions_per_page
    
    if not st.session_state.show_results:
        # Progress bar
        progress = (st.session_state.current_page * questions_per_page) / len(questions)
        st.progress(progress)
        
        # Display current page questions
        start_idx = st.session_state.current_page * questions_per_page
        end_idx = min(start_idx + questions_per_page, len(questions))
        
        for i in range(start_idx, end_idx):
            display_question(questions[i], i)
        
        # Navigation
        # col1, col2, col3 = st.columns([1, 2, 1])
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.session_state.current_page > 0:
                if st.button("← Previous", use_container_width=True):
                    st.session_state.current_page -= 1
                    st.rerun()
        
        with col2:
            st.markdown(f"""
                <div style='text-align: center;'>
                    Page {st.session_state.current_page + 1} of {total_pages}
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if st.session_state.current_page < total_pages - 1:
                if st.button("Next →", use_container_width=True):
                    st.session_state.current_page += 1
                    st.rerun()
            elif st.button("Submit Quiz", type="primary", use_container_width=True):
                st.session_state.show_results = True
                st.rerun()
        
        # Submit button visible on all pages
        # st.markdown(
        #     """
        #     <div class='submit-button'>
        #         <form>
        #             <button class='stButton' type='submit' 
        #                     style='background-color: #4CAF50; color: white; 
        #                            padding: 10px 20px; border-radius: 5px; 
        #                            border: none; cursor: pointer;'>
        #                 Submit Quiz
        #             </button>
        #         </form>
        #     </div>
        #     """,
        #     unsafe_allow_html=True
        # )
        
        # Handle submit button click
        if st.button("Submit Quiz", key="submit_quiz_hidden", type="primary"):
            st.session_state.show_results = True
            st.balloons()  # Built-in Streamlit celebration effect
            confetti()  # Additional confetti effect
            st.rerun()
    
    else:
        # Calculate and display results
        correct, total, results = calculate_score(questions)
        st.balloons()  # Celebration effect when showing results
        confetti()  # Additional confetti effect
        display_results(questions, results, correct, total)
        
        if st.button("Retry Quiz", type="primary"):
            st.session_state.clear()
            st.rerun()

def calculate_score(questions):
    correct = 0
    total = len(questions)
    results = []
    
    for i, q in enumerate(questions):
        user_ans = st.session_state.user_answers.get(i, '')
        is_correct = user_ans == q['correct_answer']
        if is_correct:
            correct += 1
        results.append({
            'question': q['question'],
            'user_answer': user_ans,
            'correct_answer': q['correct_answer'],
            'is_correct': is_correct
        })
    
    return correct, total, results

if __name__ == "__main__":
    main()