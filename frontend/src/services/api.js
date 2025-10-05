// src/services/api.js
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000';

export const getNutritionInfo = async (imageFile) => {
  const formData = new FormData();
  formData.append('file', imageFile);

  try {
    const response = await axios.post(`${API_URL}/api/v1/predict/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  } catch (error) {
    console.error("Error uploading image:", error);
    throw new Error('Failed to get nutrition data. Is the backend running?');
  }
};