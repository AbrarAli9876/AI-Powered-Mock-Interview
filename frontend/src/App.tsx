import { Navigate, Route, Routes } from "react-router-dom";

import ProtectedRoute from "./components/ProtectedRoute";

import LandingPage from "./pages/LandingPage";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";

import Dashboard from "./pages/Dashboard";
import InterviewResult from "./pages/InterviewResult";
import Profile from "./pages/Profile";

import InterviewSetup from "./pages/InterviewSetup";
import InterviewPreflight from "./pages/InterviewPreflight";
import InterviewRoom from "./pages/InterviewRoom";

import CodingInterviewSetup from "./pages/CodingInterviewSetup";
import CodingInterviewPreflight from "./pages/CodingInterviewPreflight";
import CodingInterviewRoom from "./pages/CodingInterviewRoom";
import CodingInterviewHistory from "./pages/CodingInterviewHistory";
import CodingInterviewResult from "./pages/CodingInterviewResult";
import AdminDashboard from "./pages/admin/AdminDashboard";

function App() {
  return (
    <Routes>
      {/* Public routes */}
      <Route path="/" element={<LandingPage />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* User-protected routes */}
      <Route element={<ProtectedRoute requiredRole="user" />}>
        <Route path="/home" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/profile" element={<Profile />} />

        {/* Technical interview setup and mandatory sequential checks */}
        <Route path="/interviews/new" element={<InterviewSetup />} />
        <Route
          path="/interviews/preflight/:step"
          element={<InterviewPreflight />}
        />
        <Route path="/interviews/:sessionId" element={<InterviewRoom />} />
        <Route
          path="/interviews/:sessionId/result"
          element={<InterviewResult />}
        />

        {/* Coding interview setup and mandatory sequential checks */}
        <Route
          path="/coding-interview/new"
          element={<CodingInterviewSetup />}
        />
        <Route
          path="/coding-interview/preflight/:step"
          element={<CodingInterviewPreflight />}
        />
        <Route path="/coding-interview" element={<CodingInterviewRoom />} />
        <Route
          path="/coding-interview/history"
          element={<CodingInterviewHistory />}
        />
        <Route
          path="/coding-interview/results/:id"
          element={<CodingInterviewResult />}
        />
      </Route>

      {/* Admin-protected routes */}
      <Route element={<ProtectedRoute requiredRole="admin" />}>
        <Route path="/admin/dashboard" element={<AdminDashboard />} />
      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default App;
