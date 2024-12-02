import { FormEvent } from "react";
import { Order, OrderSide, OrderType } from "../hooks/use-smocks-api";
import "./OrderForm.css";

type OrderFormProps = {
  onOrder: (orderSide: OrderSide, order: Order) => void;
};

function OrderForm({ onOrder }: OrderFormProps) {
  async function handleFormSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const formElement = event.target as HTMLFormElement;
    const formData = new FormData(formElement);

    const orderSide = formData.get("orderSide") as OrderSide;

    const order: Order = {
      type: formData.get("OrderType") as OrderType,
      assetId: formData.get("assetId") as string,
      quantity: Number(formData.get("quantity")),
    };

    onOrder(orderSide, order);
  }

  return (
    <form className="smockOrderForm" onSubmit={handleFormSubmit}>
      <fieldset>
        <legend>Order Type</legend>
        <label>Buy</label>
        <input required type="radio" name="orderSide" value={OrderSide.BUY} />
        <label>Sell</label>
        <input required type="radio" name="orderSide" value={OrderSide.SELL} />
      </fieldset>
      <select name="OrderType">
        {Object.values(OrderType).map((val) => {
          return (
            <option key={val} value={val}>
              {val}
            </option>
          );
        })}
      </select>
      <input type="text" placeholder="assest id" name="assetId" />
      <input type="number" name="quantity" />
      <input type="submit" value="Place Order" />
    </form>
  );
}

export default OrderForm;
