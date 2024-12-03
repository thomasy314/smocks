import { useEffect, useState } from "react";
import useBasicAuthState from "../auth/useAuthState";
import {
  AssetType,
  SmockResponseStatus,
  useSmocksApi,
} from "../smocksApi/use-smocks-api";
import ArtistSummary from "./ArtistSummary";

type ArtistData = {
  followers: number;
  id: string;
  name: string;
  popularity: number;
  type: AssetType;
  url: string;
  images: Record<string, string>[];
};

type ArtistProps = {
  artist_id: string;
  loadingPrompt?: string;
};

function Artist({ artist_id, loadingPrompt = "loading" }: ArtistProps) {
  const { basicAuthToken } = useBasicAuthState();

  const { getArtist } = useSmocksApi(basicAuthToken ?? "");
  const [artistData, setArtistData] = useState<ArtistData | null>(null);

  useEffect(() => {
    const fetchArtist = async () => {
      const artistResult = await getArtist(artist_id);

      if (artistResult.status === SmockResponseStatus.SUCCESS) {
        setArtistData(artistResult.data);
      } else {
        setArtistData(null);
      }
    };

    fetchArtist();
  }, [artist_id]);

  return (
    <>
      {artistData ? (
        <ArtistSummary artistData={artistData} />
      ) : (
        <p>{loadingPrompt}</p>
      )}
    </>
  );
}

export default Artist;
export type { ArtistData };
