import LogoutButton from "../auth/LogoutButton";
import useSmocksData from "../smocksApi/use-smocks-data";
import AccountSummary from "./AccountSummary";
import Positions from "./Positions";

function AccountPage() {
  const { accountData, positionsData } = useSmocksData();

  return (
    <main style={{ textAlign: "center" }}>
      <h1>Account</h1>
      {accountData ? (
        <>
          <AccountSummary accountData={accountData} />
          <LogoutButton />
        </>
      ) : (
        <p>Loading account info...</p>
      )}
      <h2>Positions</h2>
      <Positions positions={positionsData} />
    </main>
  );
}

export default AccountPage;
