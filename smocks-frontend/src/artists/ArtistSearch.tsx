import { useState } from "react";
import Artist from "./Artist";

function ArtistSearch() {
  const [artistId, setArtistId] = useState("");

  return (
    <>
      <input
        type="text"
        value={artistId}
        placeholder="Search for artist"
        onChange={(event) => setArtistId(event.target.value)}
      />
      <Artist artist_id={artistId} loadingPrompt="" />
    </>
  );
}

export default ArtistSearch;
