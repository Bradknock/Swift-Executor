"use client";
import { useState, useEffect } from "react";

export default function Home() {
  const [prediction, setPrediction] = useState(null);

  // Function to fetch the prediction value
  const fetchPrediction = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/get_prediction");
      if (response.ok) {
        const data = await response.json();
        setPrediction(data.prediction_value);

        // Print true if prediction is 1, otherwise print false
        console.log(data.prediction_value === 1 ? "true" : "false");
      } else {
        console.error("Failed to fetch prediction");
      }
    } catch (error) {
      console.error("Error fetching prediction:", error);
    }
  };

  useEffect(() => {
    fetchPrediction();
  }, []);

  return (
    <div>
      <h1>Prediction Value:</h1>
      <p>{prediction !== null ? prediction : "No prediction available"}</p>
      <button onClick={fetchPrediction}>Refresh Prediction</button>
    </div>
  );
}
