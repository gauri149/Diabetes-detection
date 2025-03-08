import numpy as np
import pickle
import streamlit as st

#Load the saved model
loaded_model = pickle.load(open('C:/Users/shekh/Desktop/Conference/Project/trained_model.sav', 'rb'))

# Function to predict diabetes risk and give personalized recommendations
def diabetes_prediction(input_data):
    input_data_as_numpy_array = np.asarray(input_data).reshape(1, -1)
 
    # Predict probability of diabetes
    risk_probability = loaded_model.predict_proba(input_data_as_numpy_array)[0][1]

    # Personalized recommendations based on high-risk factors
    recommendations = []

    #Add personalized recommendations based on each factor
    if input_data[0] > 6: 
        #Pregnancies
        recommendations.append("Consider consulting with a healthcare provider about gestational diabetes.")
    if input_data[1] > 140:
        #Glucose level 
        recommendations.append("Reduce sugar intake and monitor glucose levels regularly.")
    if input_data[2] > 80:
        #Blood Pressure
        recommendations.append("Maintain a balanced diet and monitor blood pressure regularly.")
    if input_data[3] > 30:
        # Skin Thickness
        recommendations.append("Consider regular health check-ups to assess skin fold thickness.")
    if input_data[4] > 160:
        #Insulin level
        recommendations.append("Consult a doctor to manage insulin levels.")
    if input_data[5] > 25:
        #BMI
        recommendations.append("Incorporate regular physical activity to lower BMI.")
    if input_data[6] > 0.5:
        #Diabetes Pedigree Function
        recommendations.append("Monitor family history and adopt preventive measures.")
    if input_data[7] > 50:
        # Age
        recommendations.append("Age is a risk factor; maintain a healthy lifestyle and regular health check-ups.")

    # Simulate risk progression over 5 years
    def risk_progression_simulation(current_risk): 
        progression= []
        for year in range(1, 6):
            future_risk=min(current_risk + (year * 0.05 * current_risk), 1)
            progression.append(f"Year {year}: {future_risk * 100:.2f}%")
        return progression
    future_risk = risk_progression_simulation(risk_probability)

    #Format the output
    diagnosis = f"Current Risk of Diabetes: {risk_probability * 100:.2f}%"
    diagnosis += "\n\nProjected Risk Progression over the next 5 years:\n" + "\n".join(future_risk)
    if recommendations:
        diagnosis += "\n\nRecommendations:\n" + "\n".join(recommendations)
    return diagnosis, risk_probability # Return diagnosis and risk probability

#Main function for Streamlit app
def main():
    st.title('Diabetes Risk Progression and Personalized Recommendations App')

    # Input fields for user data and convert to numeric types
    Pregnancies = st.text_input('Number of Pregnancies')
    Glucose = st.text_input('Glucose Level')
    BloodPressure = st.text_input('Blood Pressure')
    SkinThickness = st.text_input('Skin Thickness')
    Insulin = st.text_input('Insulin Level')
    BMI = st.text_input('BMI')
    DiabetesPedigreeFunction = st.text_input ('Diabetes Pedigree Function')
    Age = st.text_input('Age')

    # Prediction button
    if st.button('Predict Diabetes Risk'):
        try:
            #Convert inputs to float or int where appropriate
            input_data = [
                float (Pregnancies),
                float (Glucose),
                float (BloodPressure),
                float (SkinThickness),
                float (Insulin),
                float (BMI),
                float (DiabetesPedigreeFunction),
                float (Age)
            ]
        
            diagnosis, risk_probability = diabetes_prediction(input_data)
            st.success(diagnosis)

            #Check if the risk is high and provide the booking link
            if risk_probability > 0.5: # Example threshold for high risk
                st.write("You are at high risk for diabetes. Please consider getting a diabetes test.") 
                st.markdown("[Book a Diabetes Test Here](https://www.1mg.com/labs/test/diabetes-screening-hba1c-fasting-sugar-1680?wpsrc=Google+Organic+Search)")
        except ValueError:
            st.error("Please enter valid numeric values for all inputs.")

if __name__ == '__main__':
    main()