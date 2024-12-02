import { useNavigate } from "react-router-dom";
import BasicAuthLogin from "../components/BasicAuthLogin";
import {
  SmockResponseStatus,
  useSmocksNoAuthApi,
} from "../hooks/use-smocks-api";

function RegisterPage() {
  const { register } = useSmocksNoAuthApi();
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
      <h1 style={{ textAlign: "center" }}>Register</h1>
      <BasicAuthLogin
        checkLoginFunc={handleRegister}
        onLoginSuccessful={onRegisterSuccessful}
      />
    </>
  );
}

export default RegisterPage;
