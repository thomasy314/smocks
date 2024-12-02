import { useLocalStorage } from "usehooks-ts";
import { BASIC_AUTH_STORAGE_KEY } from "./auth/auth.constants";

function LandingPage() {
  const [basicAuthToken] = useLocalStorage(BASIC_AUTH_STORAGE_KEY, null, {
    deserializer: (val) => val,
  });

  console.log(basicAuthToken);

  return (
    <main style={{ textAlign: "center" }}>
      <h1>SMOCKS!</h1>
      {basicAuthToken ? (
        <a href="/account">Account Dashboard</a>
      ) : (
        <>
          <a href="/login">Login</a>
          <br />
          <a href="/register">Create Account</a>
        </>
      )}
    </main>
  );
}

export default LandingPage;
