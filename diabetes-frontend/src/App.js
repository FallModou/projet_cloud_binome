import React, { useState } from "react";
import "./App.css";

function App() {
  const [formData, setFormData] = useState({
    Pregnancies: 1,
    Glucose: 100,
    BloodPressure: 70,
    SkinThickness: 20,
    Insulin: 80,
    BMI: 25.0,
    DiabetesPedigreeFunction: 0.5,
    Age: 30
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: Number(value)
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setPrediction(null);
    try {
      const response = await fetch("http://backend:8000/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      setPrediction(data.prediction);
    } catch (error) {
      console.error("Erreur:", error);
      setPrediction("Erreur lors de la prédiction");
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <h1>Prédiction du diabète</h1>
      <form onSubmit={handleSubmit}>
        {Object.keys(formData).map((key) => (
          <div className="form-group" key={key}>
            <label>{key}</label>
            <input
              type="number"
              name={key}
              value={formData[key]}
              onChange={handleChange}
              min={0}
              step="any"
            />
          </div>
        ))}
        <button type="submit" disabled={loading}>
          {loading ? "Chargement..." : "Prédire"}
        </button>
      </form>
      {prediction !== null && (
        <div className="result">
          <h2>Résultat :</h2>
          <p>{prediction === 1 ? "Diabétique" : prediction === 0 ? "Non diabétique" : prediction}</p>
        </div>
      )}
    </div>
  );
}

export default App;
