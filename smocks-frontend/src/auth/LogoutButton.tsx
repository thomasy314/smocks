import { useNavigate } from "react-router-dom";
import { useSmocksNoAuthApi } from "../hooks/use-smocks-api";

function LogoutButton() {
  const { logout } = useSmocksNoAuthApi();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/");
  }

  return <button onClick={handleLogout}>Logout</button>;
}

export default LogoutButton;
