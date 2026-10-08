import React from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import UploadQuiz from './pages/UploadQuiz'
import QuizTaker from './pages/QuizTaker'
import Results from './pages/Results'

export default function App(){
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Navigate to="/upload" replace />} />
        <Route path="/upload" element={<UploadQuiz />} />
        <Route path="/quiz/:id" element={<QuizTaker />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </BrowserRouter>
  )
}
