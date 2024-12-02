import { PropsWithChildren, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import useBasicAuthState from "../auth/useAuthState";

type RequireBasicAuthProps = {};

function PrivateRoute({ children }: PropsWithChildren<RequireBasicAuthProps>) {
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
