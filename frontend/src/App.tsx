import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import Landing from "./pages/Landing";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import InterviewSetup from "./pages/InterviewSetup";
import AdminDashboard from "./pages/admin/AdminDashboard";

import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Public */}

        <Route
          path="/"
          element={<Landing />}
        />

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />


        {/* Candidate */}

        <Route
          element={
            <ProtectedRoute requiredRole="user" />
          }
        >

          <Route
            path="/home"
            element={<Home />}
          />

          <Route
            path="/interviews/new"
            element={<InterviewSetup />}
          />

        </Route>


        {/* Admin */}

        <Route
          element={
            <ProtectedRoute requiredRole="admin" />
          }
        >

          <Route
            path="/admin"
            element={<AdminDashboard />}
          />

        </Route>


        {/* Fallback */}

        <Route
          path="*"
          element={
            <Navigate
              to="/"
              replace
            />
          }
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;