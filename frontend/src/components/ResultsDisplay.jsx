// src/components/ResultsDisplay.jsx
import React from 'react';
import './ResultsDisplay.css';

const ResultsDisplay = ({ data, isLoading, error, onReset }) => {
  if (isLoading) {
    return <div className="loader"></div>;
  }

  // THIS IS THE FIX: The button is now inside this 'if' block
  if (error) {
    return (
      <div className="error-message">
        <span>⚠️ {error}</span>
        <button onClick={onReset} className="reset-button">
          Try Again
        </button>
      </div>
    );
  }

  if (!data) {
    return <div className="info-message">Upload an image and click "Analyze Meal" to see the nutritional facts.</div>;
  }

  const { total_nutrition, items } = data;

  return (
    <div className="results-container">
      <h2>Total nutrition</h2>
      <div className="nutrition-card">
        <div className="nutrition-item"><span className="nutrient-label">Calories</span><span className="nutrient-value">{total_nutrition.calories}</span></div>
        <div className="nutrition-item"><span className="nutrient-label">Protein (g)</span><span className="nutrient-value">{total_nutrition.protein_g}</span></div>
        <div className="nutrition-item"><span className="nutrient-label">Fat (g)</span><span className="nutrient-value">{total_nutrition.fat_g}</span></div>
        <div className="nutrition-item"><span className="nutrient-label">Carbs (g)</span><span className="nutrient-value">{total_nutrition.carbs_g}</span></div>
      </div>

      {Array.isArray(items) && items.length > 0 && (
        <>
          <h3>Items</h3>
          <div className="nutrition-card">
            {items.map((it, idx) => (
              <div className="nutrition-item" key={`${it.food_name}-${idx}`}>
                <span className="nutrient-label">{it.food_name}</span>
                <span className="nutrient-value">{`${it.calories} kcal, P ${it.protein_g}g, F ${it.fat_g}g, C ${it.carbs_g}g`}</span>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
};

export default ResultsDisplay;