import { Navigate, Outlet } from "react-router-dom";

interface ProtectedRouteProps {
  requiredRole?: "admin" | "user";
}

export default function ProtectedRoute({
  requiredRole,
}: ProtectedRouteProps) {
  const token =
    localStorage.getItem("access_token");

  const userData =
    localStorage.getItem("user");

  if (!token || !userData) {
    return (
      <Navigate
        to="/login"
        replace
      />
    );
  }

  try {
    const user = JSON.parse(userData);

    if (
      requiredRole &&
      user.role !== requiredRole
    ) {
      if (user.role === "admin") {
        return (
          <Navigate
            to="/admin"
            replace
          />
        );
      }

      return (
        <Navigate
          to="/dashboard"
          replace
        />
      );
    }

    return <Outlet />;

  } catch {
    localStorage.removeItem(
      "access_token"
    );

    localStorage.removeItem(
      "user"
    );

    return (
      <Navigate
        to="/login"
        replace
      />
    );
  }
}