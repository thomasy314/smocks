import Positions from "../account/Positions";
import useBasicAuthState from "../auth/useAuthState";
import { Order, OrderSide, useSmocksApi } from "../hooks/use-smocks-api";
import useSmocksData from "../hooks/use-smocks-data";
import OrderForm from "./OrderForm";

function OrderPage() {
  const { basicAuthToken } = useBasicAuthState();

  const { createPurchaseOrder } = useSmocksApi(basicAuthToken ?? "");

  const {
    accountData,
    positionsData,
    refreshPositionData,
    refreshAccountData,
  } = useSmocksData();

  async function handleOrder(orderSide: OrderSide, order: Order) {
    switch (orderSide) {
      case OrderSide.BUY:
        const orderResult = await createPurchaseOrder(order);
        console.log(orderResult);
        break;
      case OrderSide.SELL:
        // TODO: Add sell operation
        break;
    }

    refreshAccountData();
    refreshPositionData();
  }

  return (
    <>
      <header style={{ textAlign: "center" }}>
        {accountData ? (
          <p>balance: {accountData.balance}</p>
        ) : (
          <p>Loading balance</p>
        )}
      </header>
      <main style={{ textAlign: "center", display: "flex" }}>
        <section style={{ flex: 1 }}>
          <h1>Orders</h1>
          <OrderForm onOrder={handleOrder} />
        </section>
        <section style={{ flex: 1 }}>
          <Positions positions={positionsData} />
        </section>
      </main>
    </>
  );
}

export default OrderPage;
