import { useEffect, useState } from "react";
import { useLocalStorage } from "usehooks-ts";
import { BASIC_AUTH_STORAGE_KEY } from "../auth/auth.constants";
import { SmockResponseStatus, useSmocksApi } from "../hooks/use-smocks-api";
import AccountSummary, { AccountData } from "./AccountSummary";

function AccountPage() {
  const [basicAuthToken] = useLocalStorage<string>(BASIC_AUTH_STORAGE_KEY, "", {
    deserializer: (val) => val,
  });

  const { getMyAccount } = useSmocksApi(basicAuthToken);
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
        <AccountSummary accountData={accountData} />
      ) : (
        <p>Loading</p>
      )}
    </main>
  );
}

export default AccountPage;
