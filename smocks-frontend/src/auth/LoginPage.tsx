import { useNavigate } from "react-router-dom";
import { BASIC_AUTH_STORAGE_KEY } from "../auth/auth.constants";
import BasicAuthLogin from "../auth/BasicAuthLogin";
import {
  SmockResponseStatus,
  useSmocksNoAuthApi,
} from "../hooks/use-smocks-api";

function LoginPage() {
  const { login } = useSmocksNoAuthApi();
  const navigate = useNavigate();

  function handleLogin(username: string, password: string) {
    return login(username, password).then(
      (result) => result.status === SmockResponseStatus.SUCCESS
    );
  }

  async function onLoginSuccessful(username: string, password: string) {
    const basicAuthToken = btoa(`${username}:${password}`);

    localStorage.setItem(BASIC_AUTH_STORAGE_KEY, `${basicAuthToken}`);

    navigate("/");
  }

  return (
    <>
      <main style={{ textAlign: "center" }}>
        <h1>Login</h1>
        <BasicAuthLogin
          checkLoginFunc={handleLogin}
          onLoginSuccessful={onLoginSuccessful}
        />
        <a href="/register">Create Account</a>
      </main>
    </>
  );
}

export default LoginPage;
