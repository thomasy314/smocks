import { useEffect } from "react";
import { useSmocksApi } from "./hooks/use-smocks-api";

function App() {
  const { getArtist } = useSmocksApi("tbone", "password");

  useEffect(() => {
    getArtist("2qUmF9odIEj4H6IDO9V0C2").then(console.log);
  }, []);

  return (
    <main>
      <h1>SMOCKS!</h1>
    </main>
  );
}

export default App;
