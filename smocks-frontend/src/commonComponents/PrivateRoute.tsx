import { PropsWithChildren, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import useBasicAuthState from "../auth/useAuthState";

function PrivateRoute({ children }: PropsWithChildren) {
  const { basicAuthToken } = useBasicAuthState();
  const navigate = useNavigate();

  useEffect(() => {
    if (basicAuthToken === null) {
      navigate("/login");
    }
  }, []);

  return <>{children}</>;
}

export default PrivateRoute;
