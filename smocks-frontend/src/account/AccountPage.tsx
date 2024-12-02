import { FC, useEffect, useState } from "react";
import LogoutButton from "../auth/LogoutButton";
import useBasicAuthState from "../auth/useAuthState";
import ElementList from "../commonComponents/ElementList";
import { SmockResponseStatus, useSmocksApi } from "../hooks/use-smocks-api";
import AccountSummary, { AccountData } from "./AccountSummary";
import PositionSummary, { PositionData } from "./PositionSummary";

function AccountPage() {
  const { basicAuthToken } = useBasicAuthState();

  const { getMyAccount, getMyPositions } = useSmocksApi(basicAuthToken ?? "");
  const [accountData, setAccountData] = useState<AccountData | null>(null);
  const [positionsData, setPositionsData] = useState<PositionData[]>([]);

  useEffect(() => {
    if (basicAuthToken == "") return;

    const fetchAccount = async () => {
      const myAccountResults = await getMyAccount();
      const myPositionsResults = await getMyPositions();

      if (myAccountResults.status === SmockResponseStatus.SUCCESS) {
        setAccountData(myAccountResults.data as AccountData);
      }
      if (myPositionsResults.status == SmockResponseStatus.SUCCESS) {
        setPositionsData(myPositionsResults.data);
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
        <p>Loading account info...</p>
      )}
      <h2>Positions</h2>
      {positionsData ? (
        <>
          <ElementList
            element={PositionSummary as FC}
            elementAttr="positionData"
            data={positionsData as PositionData[]}
          />
        </>
      ) : (
        <p>Loading position data</p>
      )}
    </main>
  );
}

export default AccountPage;
