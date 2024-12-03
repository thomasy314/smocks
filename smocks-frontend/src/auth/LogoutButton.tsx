import { useNavigate } from "react-router-dom";
import { useNoAuthSmocksApi } from "../smocksApi/use-smocks-api";

function LogoutButton() {
  const { logout } = useNoAuthSmocksApi();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/");
  }

  return <button onClick={handleLogout}>Logout</button>;
}

export default LogoutButton;
