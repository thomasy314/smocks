import { AssetType } from "../smocksApi/use-smocks-api";
import "./PositionSummary.css";

type AssetInfoData = {
  followers: number;
  id: number;
  name: string;
  popularity: number;
  type: AssetType;
  url: string;
};

type AssetInfoProps = {
  assetInfoData: AssetInfoData;
};

type PositionData = {
  accountId: string;
  assetInfo: AssetInfoData;
  averageEntryPrice: number;
  quantity: number;
};

type PositionSummaryProps = {
  positionData: PositionData;
};

function AssetInfo({ assetInfoData: assetData }: AssetInfoProps) {
  const { followers, id, name, popularity, type, url } = assetData;
  return (
    <>
      <h3>{name}</h3>
      <small>id: {id}</small>
      <p>followers: {followers}</p>
      <p>popularity: {popularity}</p>
      <p>asset type: {type}</p>
      <a href={url}>Go to {name} on spotify</a>
    </>
  );
}

function PositionSummary({ positionData }: PositionSummaryProps) {
  const { assetInfo, averageEntryPrice, quantity } = positionData;

  return (
    <article className="positionSummaryContainer">
      <AssetInfo assetInfoData={assetInfo} />
      <p>average entry price: {averageEntryPrice}</p>
      <p>quantity: {quantity}</p>
      <p>total value: {averageEntryPrice * quantity}</p>
    </article>
  );
}

export default PositionSummary;
export type { AssetInfoData, PositionData };
