type AccountData = {
  balance: number;
  id: string;
  marketValue: number;
  username: string;
};

type AccountSummaryProps = {
  accountData: AccountData;
};

function AccountSummary({ accountData }: AccountSummaryProps) {
  return (
    <>
      <p>Username: {accountData.username}</p>
      <p>Balance: {accountData.balance}</p>
      <p>Market Value: {accountData.marketValue}</p>
    </>
  );
}

export default AccountSummary;
export type { AccountData };
