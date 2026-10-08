import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { AuthProvider } from './context/AuthContext'
import UploadQuiz from './pages/UploadQuiz'
import QuizTaker from './pages/QuizTaker'
import Results from './pages/Results'
import Login from './pages/Login'
import Signup from './pages/Signup'
import './index.css'

const queryClient = new QueryClient()

function AppRoutes(){
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/upload" replace />} />
      <Route path="/upload" element={<UploadQuiz />} />
      <Route path="/quiz/:id" element={<QuizTaker />} />
      <Route path="/results" element={<Results />} />
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />
    </Routes>
  )
}

createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <AuthProvider>
          <AppRoutes />
        </AuthProvider>
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>
)
