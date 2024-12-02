import { useNavigate } from "react-router-dom";
import BasicAuthLogin from "../commonComponents/BasicAuthLogin";
import { useSmocksNoAuthApi } from "../hooks/use-smocks-api";

function LoginPage() {
  const { login } = useSmocksNoAuthApi();
  const navigate = useNavigate();

  async function onLoginSuccessful(username: string, password: string) {
    const basicAuthToken = btoa(`${username}:${password}`);

    localStorage.setItem("basicAuthToken", `${basicAuthToken}`);

    navigate("/");
  }

  return (
    <BasicAuthLogin
      checkLoginFunc={login}
      onLoginSuccessful={onLoginSuccessful}
    />
  );
}

export default LoginPage;
