import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
} from "react-router-dom";

import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Dashboard from "./pages/Dashboard";

import AdminDashboard from "./pages/admin/AdminDashboard";

import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Public pages */}

        <Route
          path="/"
          element={<Home />}
        />

        <Route
          path="/login"
          element={<Login />}
        />

        <Route
          path="/register"
          element={<Register />}
        />


        {/* Candidate pages */}

        <Route
          element={
            <ProtectedRoute
              requiredRole="user"
            />
          }
        >
          <Route
            path="/dashboard"
            element={<Dashboard />}
          />
        </Route>


        {/* Admin pages */}

        <Route
          element={
            <ProtectedRoute
              requiredRole="admin"
            />
          }
        >
          <Route
            path="/admin"
            element={<AdminDashboard />}
          />
        </Route>


        {/* Unknown route */}

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