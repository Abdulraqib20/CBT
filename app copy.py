import streamlit as st
import pandas as pd
from collections import defaultdict
import time
from datetime import datetime, timedelta

from streamlit_confetti import confetti
import streamlit.components.v1 as components

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
            # background-color: #1F77B4;
            # color: #FFFFFF;
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


# def initialize_session_state():
#     if 'current_page' not in st.session_state:
#         st.session_state.current_page = 0
#     if 'user_answers' not in st.session_state:
#         st.session_state.user_answers = defaultdict(str)
#     if 'show_results' not in st.session_state:
#         st.session_state.show_results = False
#     if 'start_time' not in st.session_state:
#         st.session_state.start_time = datetime.now()
#     if 'time_remaining' not in st.session_state:
#         st.session_state.time_remaining = timedelta(minutes=15)

# def display_timer():
#     current_time = datetime.now()
#     elapsed_time = current_time - st.session_state.start_time
#     remaining_time = st.session_state.time_remaining - elapsed_time

#     if remaining_time.total_seconds() <= 0:
#         st.session_state.show_results = True
#         st.rerun()

#     minutes = int(remaining_time.total_seconds() // 60)
#     seconds = int(remaining_time.total_seconds() % 60)
#     st.markdown(f"""
#         <div class="timer-widget">
#             Time Remaining: {minutes:02d}:{seconds:02d}
#         </div>
#     """, unsafe_allow_html=True)


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
    if 'review_mode' not in st.session_state:  # ✅ Initialize review_mode
        st.session_state.review_mode = False  # Default value




def display_timer():
    current_time = datetime.now()
    elapsed_time = current_time - st.session_state.start_time
    remaining_time = st.session_state.time_remaining - elapsed_time
    remaining_seconds = max(int(remaining_time.total_seconds()), 0)
    
    timer_html = f"""
    <div id="timer" class="timer-widget">
        Time Remaining: <span id="time">{remaining_seconds//60:02d}:{remaining_seconds%60:02d}</span>
    </div>
    <script>
    (function() {{
        var duration = {remaining_seconds}; // duration in seconds
        var display = document.getElementById('time');
        var timer = duration, minutes, seconds;
        setInterval(function () {{
            minutes = parseInt(timer / 60, 10);
            seconds = parseInt(timer % 60, 10);
            minutes = minutes < 10 ? "0" + minutes : minutes;
            seconds = seconds < 10 ? "0" + seconds : seconds;
            display.textContent = minutes + ":" + seconds;
            if (timer > 0) {{
                timer--;
            }} else {{
                // Optional: trigger an action when time is up.
            }}
        }}, 1000);
    }})();
    </script>
    """
    components.html(timer_html, height=100)


    


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



def display_score_summary(correct, total):
    st.balloons()
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
    st.markdown("### Performance Summary")
    for key, value in performance_data.items():
        st.markdown(f"**{key}:** {value}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Review Answers"):
            st.session_state.review_mode = True
            st.session_state.current_page = 0
            st.rerun()
    with col2:
        if st.button("Retry Quiz"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()



def display_review_question(question, index, user_answers):
    st.markdown(f"""
        <div class="review-card">
            <h3>{question['question']}</h3>
        </div>
    """, unsafe_allow_html=True)
    
    user_answer = user_answers.get(index, '')
    correct_answer = question['correct_answer']
    is_correct = user_answer == correct_answer
    
    for option in question['options']:
        option_letter = option[0]
        css_class = ""
        if option_letter == correct_answer:
            css_class = "correct-answer"
        elif option_letter == user_answer and not is_correct:
            css_class = "wrong-answer"
        
        st.markdown(f"""
            <div class="{css_class}">
                {option}
                {' ✓' if option_letter == correct_answer else ' ✗' if option_letter == user_answer and not is_correct else ''}
            </div>
        """, unsafe_allow_html=True)


def main():
    load_css()
    
    # Header with credits
    st.markdown("""
        <h1 style='text-align: center;'>ABE501 MCQ Practice</h1>
        <h3 style='text-align: center;'>Management Engineering Exam Preparation</h3>
        <div class='credits'>
            Built with ❤️ by <a href='https://github.com/Abdulraqib20' target='_blank'>raqibcodes</a>
        </div>
    """, unsafe_allow_html=True)
    
    initialize_session_state()
    
    #################################################################################################################
    ################################### QUESTIONS ################################################################
    
    
    from questions import questions 
    
    
    if not questions:
        st.warning("Please add your questions to the questions list!")
        return
    
    questions_per_page = 5
    total_pages = (len(questions) + questions_per_page - 1) // questions_per_page
    
    if st.session_state.show_results and not st.session_state.review_mode:
        correct, total, _ = calculate_score(questions)
        display_score_summary(correct, total)
    
    elif st.session_state.review_mode:
        start_idx = st.session_state.current_page * questions_per_page
        end_idx = min(start_idx + questions_per_page, len(questions))
        
        for i in range(start_idx, end_idx):
            display_review_question(questions[i], i, st.session_state.user_answers)
            st.divider()
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.session_state.current_page > 0:
                if st.button("← Previous"):
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
                if st.button("Next →"):
                    st.session_state.current_page += 1
                    st.rerun()
        
        if st.button("Retry Quiz"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    
    else:
        # Create a container for the timer
        timer_container = st.container()
        with timer_container:
            display_timer()
        
        start_idx = st.session_state.current_page * questions_per_page
        end_idx = min(start_idx + questions_per_page, len(questions))
        
        for i in range(start_idx, end_idx):
            display_question(questions[i], i)
            st.divider()
        
        # Navigation and submit button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            if st.session_state.current_page > 0:
                if st.button("← Previous"):
                    st.session_state.current_page -= 1
                    st.rerun()
        
        with col2:
            st.markdown(f"""
                <div style='text-align: center;'>
                    Page {st.session_state.current_page + 1} of {total_pages}
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("Submit Quiz", type="primary", use_container_width=True):
                st.session_state.show_results = True
                st.rerun()
        
        with col3:
            if st.session_state.current_page < total_pages - 1:
                if st.button("Next →"):
                    st.session_state.current_page += 1
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