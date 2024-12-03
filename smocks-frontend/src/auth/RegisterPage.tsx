import { useNavigate } from "react-router-dom";
import BasicAuthLogin from "../auth/BasicAuthLogin";
import {
  SmockResponseStatus,
  useNoAuthSmocksApi,
} from "../smocksApi/use-smocks-api";

function RegisterPage() {
  const { register } = useNoAuthSmocksApi();
  const navigate = useNavigate();

  function handleRegister(username: string, password: string) {
    return register(username, password).then(
      (result) => result.status === SmockResponseStatus.SUCCESS
    );
  }

  async function onRegisterSuccessful(username: string, password: string) {
    navigate("/login");
  }

  return (
    <>
      <main style={{ textAlign: "center" }}>
        <h1>Register</h1>
        <BasicAuthLogin
          checkLoginFunc={handleRegister}
          onLoginSuccessful={onRegisterSuccessful}
        />
        <a href="/login">Login</a>
      </main>
    </>
  );
}

export default RegisterPage;
