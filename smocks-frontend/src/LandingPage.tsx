import LogoutButton from "./auth/LogoutButton";
import useBasicAuthState from "./auth/useAuthState";

function LandingPage() {
  const { basicAuthToken } = useBasicAuthState();

  return (
    <main style={{ textAlign: "center" }}>
      <h1>SMOCKS!</h1>
      {basicAuthToken ? (
        <>
          <a href="/account">Account Dashboard</a>
          <br />
          <LogoutButton />
        </>
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
