import { FC } from "react";
import ElementList from "../commonComponents/ElementList";
import PositionSummary, { PositionData } from "./PositionSummary";

type PositionsProps = {
  positions?: PositionData[] | null;
};

function Positions({ positions }: PositionsProps) {
  return (
    <>
      {positions ? (
        <>
          <ElementList
            element={PositionSummary as FC}
            elementAttr="positionData"
            data={positions}
          />
        </>
      ) : (
        <p>Loading positions data</p>
      )}
    </>
  );
}

export default Positions;
