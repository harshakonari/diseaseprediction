import React, { useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000";

const diseaseFields = {
  "Heart Disease": [
    "age","sex","cp","trestbps","chol","fbs","restecg",
    "thalach","exang","oldpeak","slope","ca","thal"
  ],
  "Diabetes": [
    "pregnancies","glucose","bloodpressure",
    "skinthickness","insulin","bmi","dpf"
  ],
  "Liver Disease": [
    "gender","total_bilirubin","direct_bilirubin",
    "alkaline_phosphotase","alamine_aminotransferase",
    "aspartate_aminotransferase","total_proteins",
    "albumin","albumin_globulin_ratio"
  ]
};

const fieldDetails = {

age:{label:"Your Age",hint:"Enter your age (example: 40)"},
sex:{label:"Your Gender",hint:"0 = Female , 1 = Male"},

cp:{
label:"Chest Pain Type",
hint:"0 = Typical angina, 1 = Atypical angina, 2 = Non-anginal pain, 3 = Asymptomatic"
},

trestbps:{
label:"Resting Blood Pressure",
hint:"Enter BP value (example: 120)"
},

chol:{
label:"Cholesterol Level",
hint:"Enter cholesterol value (example: 200)"
},

fbs:{
label:"Fasting Blood Sugar",
hint:"0 = Normal , 1 = High"
},

restecg:{
label:"ECG Result",
hint:"0 = Normal , 1 = Abnormality , 2 = Left ventricular hypertrophy"
},

thalach:{
label:"Maximum Heart Rate",
hint:"Example value: 150"
},

exang:{
label:"Chest Pain During Exercise",
hint:"0 = No , 1 = Yes"
},

oldpeak:{
label:"Heart Stress Level",
hint:"Example: 1.5"
},

slope:{
label:"Heart Test Slope",
hint:"0 = Upsloping , 1 = Flat , 2 = Downsloping"
},

ca:{
label:"Blocked Heart Vessels",
hint:"Number between 0 and 3"
},

thal:{
label:"Thalassemia Test",
hint:"1 = Normal , 2 = Fixed defect , 3 = Reversible defect"
},

pregnancies:{
label:"Number of Pregnancies",
hint:"Example: 2"
},

glucose:{
label:"Blood Glucose Level",
hint:"Example: 140"
},

bloodpressure:{
label:"Blood Pressure",
hint:"Example: 80"
},

skinthickness:{
label:"Skin Thickness",
hint:"Example: 20"
},

insulin:{
label:"Insulin Level",
hint:"Example: 85"
},

bmi:{
label:"Body Mass Index",
hint:"Example: 24.5"
},

dpf:{
label:"Family Diabetes History Score",
hint:"Example: 0.5"
},

gender:{
label:"Your Gender",
hint:"0 = Female , 1 = Male"
},

total_bilirubin:{
label:"Total Bilirubin",
hint:"Example: 1.0"
},

direct_bilirubin:{
label:"Direct Bilirubin",
hint:"Example: 0.3"
},

alkaline_phosphotase:{
label:"Alkaline Phosphotase",
hint:"Example: 200"
},

alamine_aminotransferase:{
label:"ALT Liver Enzyme",
hint:"Example: 35"
},

aspartate_aminotransferase:{
label:"AST Liver Enzyme",
hint:"Example: 40"
},

total_proteins:{
label:"Total Proteins",
hint:"Example: 6.5"
},

albumin:{
label:"Albumin Level",
hint:"Example: 3.5"
},

albumin_globulin_ratio:{
label:"Albumin / Globulin Ratio",
hint:"Example: 1.2"
}

};

const allFields = [
"age","sex","cp","trestbps","chol","fbs","restecg",
"thalach","exang","oldpeak","slope","ca","thal",
"pregnancies","glucose","bloodpressure","skinthickness",
"insulin","bmi","dpf",
"gender","total_bilirubin","direct_bilirubin",
"alkaline_phosphotase","alamine_aminotransferase",
"aspartate_aminotransferase","total_proteins",
"albumin","albumin_globulin_ratio"
];

function App(){

const [step,setStep]=useState("start");
const [predictFields,setPredictFields]=useState([]);
const [currentQuestion,setCurrentQuestion]=useState(0);

const [startData,setStartData]=useState({
age:"",
gender:"",
symptoms:""
});

const [formData,setFormData]=useState({});
const [answer,setAnswer]=useState("");
const [result,setResult]=useState(null);

const handleStartChange=(e)=>{
setStartData({...startData,[e.target.name]:e.target.value});
};

const startAssessment=async()=>{

const symptomsArray=startData.symptoms.split(",").map(s=>s.trim());

const res=await fetch(`${API}/start-assessment`,{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
age:parseInt(startData.age),
gender:startData.gender,
symptoms:symptomsArray
})
});

const data=await res.json();

if(data.probable_diseases.length>0){

const disease=data.probable_diseases[0];

setPredictFields(diseaseFields[disease]);
setStep("announcement");
}

};

const nextQuestion=()=>{

const field=predictFields[currentQuestion];

setFormData({
...formData,
[field]:Number(answer)
});

setAnswer("");

if(currentQuestion+1<predictFields.length){
setCurrentQuestion(currentQuestion+1);
}
else{
predictDisease();
}

};

const predictDisease=async()=>{

let payload={};

allFields.forEach(field=>{
payload[field]=formData[field] ? formData[field] : 0;
});

const res=await fetch(`${API}/predict`,{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify(payload)
});

const data=await res.json();

setResult(data.top_prediction);
setStep("result");

};

return(

<div className="app-container">
<div className="card">

<h2 className="app-title">AI Disease Predictor</h2>
<p className="app-subtitle">Quick Health Check</p>

{/* START PAGE */}

{step==="start" && (

<>

<div className="form-group">
<label>Age</label>
<input type="number" name="age" onChange={handleStartChange}/>
</div>

<div className="form-group">
<label>Gender</label>
<input type="text" name="gender" placeholder="male / female" onChange={handleStartChange}/>
</div>

<div className="form-group">
<label>Symptoms</label>
<input
type="text"
name="symptoms"
placeholder="chest pain, fatigue"
onChange={handleStartChange}
/>
</div>

<button className="button" onClick={startAssessment}>
Start Assessment
</button>

</>

)}

{/* ANNOUNCEMENT */}

{step==="announcement" && (

<div style={{textAlign:"center"}}>

<h3 style={{marginBottom:"20px"}}>Next Step</h3>

<p style={{color:"#4b5563",marginBottom:"25px",lineHeight:"1.6"}}>

Based on your symptoms, we recommend checking a few medical test
values.

Please enter the values from your medical report in the next step
so the system can give an accurate prediction.

</p>

<button
className="button"
onClick={()=>setStep("questions")}
>
Continue
</button>

</div>

)}

{/* QUESTIONS */}

{step==="questions" && (

<>

<h3 style={{marginBottom:"10px"}}>
{fieldDetails[predictFields[currentQuestion]]?.label}
</h3>

<p style={{color:"#6b7280",marginBottom:"15px"}}>
{fieldDetails[predictFields[currentQuestion]]?.hint}
</p>

<input
type="number"
value={answer}
onChange={(e)=>setAnswer(e.target.value)}
/>

<button className="button" onClick={nextQuestion}>
Next
</button>

</>

)}

{/* RESULT */}

{step==="result" && result && (

<div className="result-box">

<div className="result-disease">
{result.disease}
</div>

<div className="result-confidence">
Confidence: {(result.confidence*100).toFixed(2)}%
</div>

<div className="result-risk">
Risk Level: {result.risk_level}
</div>

</div>

)}

</div>
</div>

);

}

export default App;