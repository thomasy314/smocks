import Positions from "../account/Positions";
import ArtistSearch from "../artists/ArtistSearch";
import useBasicAuthState from "../auth/useAuthState";
import { Order, OrderSide, useSmocksApi } from "../smocksApi/use-smocks-api";
import useSmocksData from "../smocksApi/use-smocks-data";
import OrderForm from "./OrderForm";

function OrderPage() {
  const { basicAuthToken } = useBasicAuthState();

  const { createPurchaseOrder, createSaleOrder } = useSmocksApi(
    basicAuthToken ?? ""
  );

  const {
    accountData,
    positionsData,
    refreshPositionData,
    refreshAccountData,
  } = useSmocksData();

  async function handleOrder(orderSide: OrderSide, order: Order) {
    switch (orderSide) {
      case OrderSide.BUY:
        createPurchaseOrder(order);
        break;
      case OrderSide.SELL:
        createSaleOrder(order);
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
        <section>
          <ArtistSearch />
        </section>
        <section style={{ flex: 1 }}>
          <Positions positions={positionsData} />
        </section>
      </main>
    </>
  );
}

export default OrderPage;
