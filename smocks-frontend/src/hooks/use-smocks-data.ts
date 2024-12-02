import { useEffect, useState } from "react";
import { AccountData } from "../account/AccountSummary";
import { PositionData } from "../account/PositionSummary";
import useBasicAuthState from "../auth/useAuthState";
import { SmockResponseStatus, useSmocksApi } from "./use-smocks-api";

function useSmocksData() {
  const { basicAuthToken } = useBasicAuthState();

  const { getMyAccount, getMyPositions } = useSmocksApi(basicAuthToken ?? "");
  const [accountData, setAccountData] = useState<AccountData | null>(null);
  const [positionsData, setPositionsData] = useState<PositionData[] | null>(
    null
  );

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

  async function refreshPositionData(): Promise<PositionData[]> {
    const myPositionsResults = await getMyPositions();

    if (myPositionsResults.status == SmockResponseStatus.SUCCESS) {
      setPositionsData(myPositionsResults.data);
    }
    return myPositionsResults.data;
  }

  async function refreshAccountData(): Promise<AccountData> {
    const myAccountResults = await getMyAccount();

    if (myAccountResults.status === SmockResponseStatus.SUCCESS) {
      setAccountData(myAccountResults.data);
    }
    return myAccountResults.data;
  }

  return {
    accountData,
    positionsData,
    refreshAccountData,
    refreshPositionData,
  };
}

export default useSmocksData;
