import { useEffect, useState } from "react";
import { AccountData } from "../account/AccountSummary";
import { PositionData } from "../account/PositionSummary";
import useBasicAuthState from "../auth/useAuthState";
import { useSmocksApi } from "./use-smocks-api";

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

      setAccountData(myAccountResults);
      setPositionsData(myPositionsResults);
    };
    fetchAccount();
  }, []);

  async function refreshPositionData(): Promise<PositionData[]> {
    const myPositionsResults = await getMyPositions();

    setPositionsData(myPositionsResults);
    return myPositionsResults;
  }

  async function refreshAccountData(): Promise<AccountData> {
    const myAccountResults = await getMyAccount();

    setAccountData(myAccountResults);
    return myAccountResults;
  }

  return {
    accountData,
    positionsData,
    refreshAccountData,
    refreshPositionData,
  };
}

export default useSmocksData;
