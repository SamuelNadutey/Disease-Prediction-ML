import os
import pickle
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go


# Set page configuration
st.set_page_config(
    page_title="Advanced Health Assistant",
    layout="wide",
    page_icon="🏥"
)

# Custom CSS with modern styling
st.markdown("""
    <style>
    /* Main app styling */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Custom title styling */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(90deg, #4b6cb7 0%, #182848 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Card styling */
    .css-1r6slb0 {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        background-color: white;
        border-radius: 5px;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #4b6cb7;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #182848;
        transform: translateY(-2px);
    }
    
    /* Metric styling */
    .css-1r6slb0.e1tzin5v0 {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'patient_history' not in st.session_state:
    st.session_state.patient_history = []

# Load models
@st.cache_resource
def load_models():
    models = {
        'diabetes': pickle.load(open("saved models/diabetes_model.sav", 'rb')),
        'heart': pickle.load(open("saved models/heart_disease_model.sav", 'rb')),
        'parkinsons': pickle.load(open("saved models/parkinsons_model.sav", 'rb'))
    }
    return models

models = load_models()

# Sidebar navigation
with st.sidebar:
    selected = option_menu(
        'Health Assistant Dashboard',
        ['Home', 'Diabetes Prediction', 'Heart Disease Prediction', 'Parkinsons Prediction', 'Patient History'],
        icons=['house', 'activity', 'heart', 'person', 'clock-history'],
        menu_icon='hospital',
        default_index=0,
        styles={
            "container": {"padding": "5!important", "background-color": "#f8f9fa"},
            "icon": {"color": "#4b6cb7", "font-size": "25px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
            "nav-link-selected": {"background-color": "#4b6cb7"},
        }
    )

# Home Page
if selected == 'Home':
    st.markdown('<h1 class="main-title">Advanced Health Assistant</h1>', unsafe_allow_html=True)

     # Add banner image
    st.image("images/health_banner.jpg", use_column_width=True)
    
    # Dashboard Overview
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Predictions", len(st.session_state.patient_history))
    with col2:
        if st.session_state.patient_history:
            positive_cases = sum(1 for case in st.session_state.patient_history if case['result'] == 'Positive')
            st.metric("Positive Cases", positive_cases)
    with col3:
        st.metric("Models Available", "3")
    
    # Recent Activity
    st.subheader("Recent Activity")
    if st.session_state.patient_history:
        recent_df = pd.DataFrame(st.session_state.patient_history[-5:])
        st.dataframe(recent_df, use_container_width=True)
    else:
        st.info("No recent activity to display")
    
    # Basic Statistics
    if st.session_state.patient_history:
        st.subheader("Disease Distribution")
        disease_counts = pd.DataFrame(st.session_state.patient_history)['disease'].value_counts()
        fig = px.pie(values=disease_counts.values, names=disease_counts.index, title='Predictions by Disease Type')
        st.plotly_chart(fig, use_container_width=True)

# Diabetes Prediction Page
if selected == 'Diabetes Prediction':
    st.markdown('<h1 class="main-title">Diabetes Risk Assessment</h1>', unsafe_allow_html=True)
    
    # Input form
    with st.form("diabetes_form"):
        col1, col2 = st.columns(2)

        
        
        with col1:
            pregnancies = st.number_input('Number of Pregnancies', min_value=0, max_value=20)
            glucose = st.number_input('Glucose Level (mg/dL)', min_value=0, max_value=300)
            blood_pressure = st.number_input('Blood Pressure (mm Hg)', min_value=0, max_value=200)
            skin_thickness = st.number_input('Skin Thickness (mm)', min_value=0, max_value=100)
        
        with col2:
            insulin = st.number_input('Insulin Level (mu U/ml)', min_value=0, max_value=900)
            bmi = st.number_input('BMI', min_value=0.0, max_value=70.0)
            dpf = st.number_input('Diabetes Pedigree Function', min_value=0.0, max_value=3.0)
            age = st.number_input('Age', min_value=0, max_value=120)
        
        submitted = st.form_submit_button("Predict Diabetes Risk")
        
        if submitted:
            input_data = [pregnancies, glucose, blood_pressure, skin_thickness, 
                         insulin, bmi, dpf, age]
            prediction = models['diabetes'].predict([input_data])[0]
            
            # Store prediction in history
            st.session_state.patient_history.append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'disease': 'Diabetes',
                'result': 'Positive' if prediction == 1 else 'Negative',
                'details': {
                    'glucose': glucose,
                    'bmi': bmi,
                    'age': age
                }
            })
            
            # Display result with custom styling
            if prediction == 1:
                st.error("⚠️ High Risk: Diabetes indicators detected")
                st.markdown("""
                    ### Recommended Actions:
                    1. Schedule an appointment with an endocrinologist
                    2. Monitor blood glucose levels regularly
                    3. Review diet and exercise habits
                    4. Consider diabetes screening tests
                """)
            else:
                st.success("✅ Low Risk: No diabetes indicators detected")
                st.markdown("""
                    ### Preventive Measures:
                    1. Maintain a healthy diet
                    2. Regular exercise
                    3. Annual health check-ups
                    4. Monitor blood sugar levels
                """)
            
            # Risk factors analysis
            st.subheader("Risk Factor Analysis")
            risk_factors = []
            if glucose > 140: risk_factors.append(("High Glucose", glucose, "mg/dL"))
            if bmi > 30: risk_factors.append(("High BMI", bmi, "kg/m²"))
            if blood_pressure > 140: risk_factors.append(("High Blood Pressure", blood_pressure, "mm Hg"))
            
            if risk_factors:
                for factor, value, unit in risk_factors:
                    st.warning(f"⚠️ {factor}: {value} {unit}")

# Heart Disease Prediction Page
if selected == 'Heart Disease Prediction':
    st.markdown('<h1 class="main-title">Heart Disease Risk Assessment</h1>', unsafe_allow_html=True)
    
    with st.form("heart_disease_form"):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age = st.number_input('Age', min_value=0, max_value=120)
            sex = st.selectbox('Sex', ['0: Female', '1: Male'])
            cp = st.selectbox('Chest Pain Type', 
                            ['0: Typical Angina', 
                             '1: Atypical Angina',
                             '2: Non-anginal Pain',
                             '3: Asymptomatic'])
            trestbps = st.number_input('Resting Blood Pressure (mm Hg)', min_value=0, max_value=200)
        
        with col2:
            chol = st.number_input('Serum Cholesterol (mg/dl)', min_value=0, max_value=600)
            fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl', ['0: No', '1: Yes'])
            restecg = st.selectbox('Resting ECG Results', 
                                 ['0: Normal',
                                  '1: ST-T Wave Abnormality',
                                  '2: Left Ventricular Hypertrophy'])
            thalach = st.number_input('Maximum Heart Rate', min_value=0, max_value=250)
        
        with col3:
            exang = st.selectbox('Exercise Induced Angina', ['0: No', '1: Yes'])
            oldpeak = st.number_input('ST Depression Induced by Exercise', min_value=0.0, max_value=10.0)
            slope = st.selectbox('Slope of Peak Exercise ST Segment', 
                               ['0: Upsloping', '1: Flat', '2: Downsloping'])
            ca = st.number_input('Number of Major Vessels', min_value=0, max_value=4)
            thal = st.selectbox('Thalassemia', ['0: Normal', '1: Fixed Defect', '2: Reversible Defect'])
        
        submitted = st.form_submit_button("Predict Heart Disease Risk")
        
        if submitted:
            # Extract numeric values from selection boxes
            sex = int(sex[0])
            cp = int(cp[0])
            fbs = int(fbs[0])
            restecg = int(restecg[0])
            exang = int(exang[0])
            slope = int(slope[0])
            thal = int(thal[0])
            
            input_data = [age, sex, cp, trestbps, chol, fbs, restecg, thalach,
                         exang, oldpeak, slope, ca, thal]
            
            prediction = models['heart'].predict([input_data])[0]
            
            # Store prediction in history
            st.session_state.patient_history.append({
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'disease': 'Heart Disease',
                'result': 'Positive' if prediction == 1 else 'Negative',
                'details': {
                    'age': age,
                    'blood_pressure': trestbps,
                    'cholesterol': chol
                }
            })
            
            if prediction == 1:
                st.error("⚠️ High Risk: Heart disease indicators detected")
                st.markdown("""
                    ### Recommended Actions:
                    1. Consult a cardiologist immediately
                    2. Regular blood pressure monitoring
                    3. Cholesterol management
                    4. Lifestyle modifications
                """)
            else:
                st.success("✅ Low Risk: No heart disease indicators detected")
                st.markdown("""
                    ### Preventive Measures:
                    1. Regular exercise
                    2. Heart-healthy diet
                    3. Stress management
                    4. Regular check-ups
                """)
            
            # Risk visualization
            st.subheader("Key Metrics Visualization")
            
            # Create radar chart for key metrics
            categories = ['Blood Pressure', 'Cholesterol', 'Heart Rate']
            values = [trestbps, chol, thalach]
            
            # Normalize values for visualization
            max_values = [200, 600, 250]  # Maximum expected values
            normalized_values = [v/m for v, m in zip(values, max_values)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=normalized_values,
                theta=categories,
                fill='toself',
                name='Patient Metrics'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)

# Parkinson's Prediction Page
if selected == "Parkinsons Prediction":
    st.markdown('<h1 class="main-title">Parkinson\'s Disease Assessment</h1>', unsafe_allow_html=True)
    
    # Add tabs for different input methods
    tab1, tab2 = st.tabs(["Manual Input", "Audio Analysis"])
    
    with tab1:
        with st.form("parkinsons_form"):
            col1, col2, col3 = st.columns(3)
            
            # Organize inputs into meaningful groups
            with col1:
                st.subheader("Frequency Measurements")
                fo = st.number_input('Average Vocal Fundamental Frequency (Hz)', key='fo')
                fhi = st.number_input('Maximum Vocal Fundamental Frequency (Hz)', key='fhi')
                flo = st.number_input('Minimum Vocal Fundamental Frequency (Hz)', key='flo')
            
            with col2:
                st.subheader("Variation Measurements")
                Jitter_percent = st.number_input('Jitter Percentage (%)', key='jitter_percent')
                Jitter_Abs = st.number_input('Absolute Jitter', key='jitter_abs')
                RAP = st.number_input('Relative Amplitude Perturbation', key='rap')
                PPQ = st.number_input('Period Perturbation Quotient', key='ppq')
                DDP = st.number_input('Average Absolute Difference', key='ddp')
            
            with col3:
                st.subheader("Additional Measurements")
                spread1 = st.number_input('Spread1', key='spread1')
                spread2 = st.number_input('Spread2', key='spread2')
                D2 = st.number_input('D2', key='d2')
                PPE = st.number_input('PPE', key='ppe')
                
            col4, col5 = st.columns(2)
            
            with col4:
                st.subheader("Shimmer Measurements")
                Shimmer = st.number_input('MDVP:Shimmer', key='shimmer')
                Shimmer_dB = st.number_input('MDVP:Shimmer(dB)', key='shimmer_db')
                APQ3 = st.number_input('Shimmer:APQ3', key='apq3')
                APQ5 = st.number_input('Shimmer:APQ5', key='apq5')
                APQ = st.number_input('MDVP:APQ', key='apq')
                DDA = st.number_input('Shimmer:DDA', key='dda')
            
            with col5:
                st.subheader("Voice Measurements")
                NHR = st.number_input('Noise to Harmonic Ratio', key='nhr')
                HNR = st.number_input('Harmonic to Noise Ratio', key='hnr')
                RPDE = st.number_input('RPDE', key='rpde')
                DFA = st.number_input('DFA', key='dfa')
            
            submitted = st.form_submit_button("Analyze Voice Parameters")
            
            if submitted:
                input_data = [fo, fhi, flo, Jitter_percent, Jitter_Abs,
                            RAP, PPQ, DDP, Shimmer, Shimmer_dB, APQ3, APQ5,
                            APQ, DDA, NHR, HNR, RPDE, DFA, spread1, spread2, D2, PPE]
                
                prediction = models['parkinsons'].predict([input_data])[0]
                
                # Store prediction in history
                st.session_state.patient_history.append({
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'disease': 'Parkinsons',
                    'result': 'Positive' if prediction == 1 else 'Negative',
                    'details': {
                        'fundamental_frequency': fo,
                        'jitter_percent': Jitter_percent,
                        'shimmer': Shimmer
                    }
                })
                
                if prediction == 1:
                    st.error("⚠️ Warning: Parkinson's disease indicators detected")
                    st.markdown("""
                        ### Recommended Actions:
                        1. Consult a neurologist
                        2. Schedule a comprehensive neurological examination
                        3. Consider additional diagnostic tests
                        4. Begin monitoring symptoms systematically
                    """)
                    
                    # Display voice analysis metrics
                    st.subheader("Voice Analysis Metrics")
                    metrics_fig = go.Figure()
                    
                    # Add voice metrics visualization
                    categories = ['Jitter', 'Shimmer', 'HNR', 'RPDE', 'DFA']
                    values = [Jitter_percent, Shimmer, HNR, RPDE, DFA]
                    
                    metrics_fig.add_trace(go.Scatterpolar(
                        r=values,
                        theta=categories,
                        fill='toself',
                        name='Voice Metrics'
                    ))
                    
                    metrics_fig.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, max(values)]
                            )),
                        showlegend=False
                    )
                    
                    st.plotly_chart(metrics_fig, use_container_width=True)
                    
                else:
                    st.success("✅ No significant Parkinson's disease indicators detected")
                    st.markdown("""
                        ### Preventive Measures:
                        1. Regular exercise
                        2. Balanced diet
                        3. Regular check-ups
                        4. Monitor for any changes in movement or speech
                    """)
    
    with tab2:
        st.info("🎤 Audio Analysis Feature (Coming Soon)")
        st.markdown("""
            This feature will allow direct voice recording and analysis for Parkinson's screening.
            Planned capabilities include:
            - Real-time voice recording
            - Automatic voice parameter extraction
            - Instant analysis and results
            - Historical voice pattern comparison
        """)

# Patient History Page
if selected == "Patient History":
    st.markdown('<h1 class="main-title">Patient History and Analytics</h1>', unsafe_allow_html=True)
    
    if not st.session_state.patient_history:
        st.info("No patient history available yet. Make some predictions to see them here!")
    else:
        # Convert history to DataFrame for analysis
        history_df = pd.DataFrame(st.session_state.patient_history)
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Assessments", len(history_df))
        with col2:
            st.metric("Unique Diseases", len(history_df['disease'].unique()))
        with col3:
            positive_rate = (history_df['result'] == 'Positive').mean() * 100
            st.metric("Positive Rate", f"{positive_rate:.1f}%")
        
        # Time series analysis
        st.subheader("Prediction Timeline")
        history_df['timestamp'] = pd.to_datetime(history_df['timestamp'])
        timeline_fig = px.line(history_df, x='timestamp', y=history_df['result'].map({'Positive': 1, 'Negative': 0}),
                             color='disease', title='Prediction Results Over Time')
        st.plotly_chart(timeline_fig, use_container_width=True)
        
        # Disease distribution
        st.subheader("Disease Distribution")
        disease_dist = px.pie(history_df, names='disease', title='Assessments by Disease Type')
        st.plotly_chart(disease_dist, use_container_width=True)
        
        # Detailed history table
        st.subheader("Detailed History")
        st.dataframe(
            history_df.sort_values('timestamp', ascending=False),
            use_container_width=True
        )
        
        # Export functionality
        if st.button("Export History to CSV"):
            csv = history_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="health_assistant_history.csv",
                mime="text/csv"
            )

# Add footer
st.markdown("""
    <div style='text-align: center; color: #666; padding: 20px;'>
        <p>Advanced Health Assistant v2.0 | Built with Streamlit</p>
        <p>Disclaimer: This is a screening tool and should not replace professional medical advice.</p>
    </div>
""", unsafe_allow_html=True)
