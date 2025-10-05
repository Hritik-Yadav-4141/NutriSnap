// src/App.jsx
import React, { useState } from 'react';
import ImageUpload from './components/ImageUpload';
import ResultsDisplay from './components/ResultsDisplay';
import { getNutritionInfo } from './services/api';
import './App.css';

function App() {
  const [selectedImage, setSelectedImage] = useState(null);
  const [nutritionData, setNutritionData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  // NEW: State to force-reset the ImageUpload component
  const [resetKey, setResetKey] = useState(0);

  const handleImageUpload = (file) => {
    setSelectedImage(file);
    setNutritionData(null);
    setError('');
  };

  const handleAnalyze = async () => {
    if (!selectedImage) {
      setError('Please upload an image first.');
      return;
    }
    setIsLoading(true);
    setError('');
    setNutritionData(null);
    try {
      const data = await getNutritionInfo(selectedImage);
      setNutritionData(data);
    } catch (err) {
      setError(err.message || 'An unknown error occurred.');
    } finally {
      setIsLoading(false);
    }
  };

  // NEW: Function to reset the entire app state
  const handleReset = () => {
    setSelectedImage(null);
    setNutritionData(null);
    setIsLoading(false);
    setError('');
    setResetKey(prevKey => prevKey + 1); // Change key to trigger re-render
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🥗 NutriSnap 📸</h1>
        <p>Snap a picture of your food to get instant nutritional insights!</p>
      </header>
      <main>
        {/* NEW: Added the key prop */}
        <ImageUpload
          key={resetKey}
          onImageUpload={handleImageUpload}
          onAnalyze={handleAnalyze}
          isLoading={isLoading}
        />
        <ResultsDisplay
          data={nutritionData}
          isLoading={isLoading}
          error={error}
          // NEW: Pass the reset function to the component
          onReset={handleReset}
        />
      </main>
      <footer className="App-footer">
        <p>Built for your Hackathon with ❤️</p>
      </footer>
    </div>
  );
}

export default App;