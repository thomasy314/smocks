import { useEffect, useState } from "react";
import LogoutButton from "../auth/LogoutButton";
import useBasicAuthState from "../auth/useAuthState";
import { SmockResponseStatus, useSmocksApi } from "../hooks/use-smocks-api";
import AccountSummary, { AccountData } from "./AccountSummary";

function AccountPage() {
  const { basicAuthToken } = useBasicAuthState();

  const { getMyAccount } = useSmocksApi(basicAuthToken ?? "");
  const [accountData, setAccountData] = useState<AccountData | null>(null);

  useEffect(() => {
    if (basicAuthToken == "") return;

    const fetchAccount = async () => {
      const result = await getMyAccount();

      if (result.status === SmockResponseStatus.SUCCESS) {
        setAccountData(result.data as AccountData);
      }
    };
    fetchAccount();
  }, []);

  return (
    <main style={{ textAlign: "center" }}>
      <h1>Account</h1>
      {accountData ? (
        <>
          <AccountSummary accountData={accountData} />
          <LogoutButton />
        </>
      ) : (
        <p>Loading</p>
      )}
    </main>
  );
}

export default AccountPage;
