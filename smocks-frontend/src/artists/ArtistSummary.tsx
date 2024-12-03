import { ArtistData } from "./Artist";

type ArtistSummaryProps = {
  artistData: ArtistData;
};

function ArtistSummary({ artistData }: ArtistSummaryProps) {
  const { name, id, followers, popularity, url } = artistData;
  return (
    <article
      style={{
        border: "3px solid black",
        borderRadius: "20px",
        padding: "10px",
        margin: "20px",
      }}
    >
      <h3>{name}</h3>
      <small>{id}</small>
      <p>followers: {followers}</p>
      <p>popularity: {popularity}</p>
      <a href={url}>View {name} on spotify</a>
    </article>
  );
}

export default ArtistSummary;
