import { PropsWithChildren, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useLocalStorage } from "usehooks-ts";

type RequireBasicAuthProps = {};

function PrivateRoute({ children }: PropsWithChildren<RequireBasicAuthProps>) {
  const [basicAuthToken] = useLocalStorage("basicAuthToken", null, {
    deserializer: (val) => val,
  });
  const navigate = useNavigate();

  useEffect(() => {
    if (basicAuthToken === null) {
      navigate("/login");
    }
  });

  return <>{children}</>;
}

export default PrivateRoute;
