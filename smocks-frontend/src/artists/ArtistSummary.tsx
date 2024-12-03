import { CSSProperties } from "react";
import { ArtistData } from "./Artist";

type ArtistSummaryProps = {
  artistData: ArtistData;
  showImage?: boolean;
};

function ArtistSummary({ artistData, showImage = true }: ArtistSummaryProps) {
  const { name, id, followers, popularity, url, images } = artistData;

  const image = images[images.length - 1];

  const imageStyle: CSSProperties = {
    maxWidth: "150px",
    height: "auto",
    width: "auto",
    display: "block",
    marginLeft: "auto",
    marginRight: "auto",
    marginBottom: "20px",
    clipPath: "circle()",
  };

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
      {image && (
        <img
          style={imageStyle}
          src={image["url"]}
          alt={`${name} profile photo`}
        />
      )}
      <small>{id}</small>
      <p>followers: {followers}</p>
      <p>popularity: {popularity}</p>
      <a href={url}>View {name} on spotify</a>
    </article>
  );
}

export default ArtistSummary;
