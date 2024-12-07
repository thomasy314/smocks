import { FC } from "react";

type ElementListProps = {
  element: FC;
  elementAttr: string;
  data: Record<string, object | string>[];
  idKey?: string;
};

function ElementList({
  element: Element,
  elementAttr,
  idKey = "id",
  data,
}: ElementListProps) {
  const items = data.map((d) => {
    return <Element key={d[idKey] as string} {...{ [elementAttr]: d }} />;
  });

  return <>{items}</>;
}

export default ElementList;
