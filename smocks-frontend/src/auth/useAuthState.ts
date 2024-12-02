import { useSyncExternalStore } from "react";
import { BASIC_AUTH_STORAGE_KEY } from "./auth.constants";

function useBasicAuthState() {
  const basicAuthTokenStore = {
    getSnapshot: () => localStorage.getItem(BASIC_AUTH_STORAGE_KEY),
    subscribe: (listener: () => void) => {
      window.addEventListener("storage", listener);
      return () => void window.removeEventListener("storage", listener);
    },
  };

  const basicAuthToken = useSyncExternalStore(
    basicAuthTokenStore.subscribe,
    basicAuthTokenStore.getSnapshot
  );

  function setBasciAuthToken(newAuthToken: string) {
    window.localStorage.setItem(BASIC_AUTH_STORAGE_KEY, newAuthToken);
    // On localStoage.setItem, the storage event is only triggered on other tabs and windows.
    // So we manually dispatch a storage event to trigger the subscribe function on the current window as well.
    window.dispatchEvent(
      new StorageEvent("storage", {
        key: BASIC_AUTH_STORAGE_KEY,
        newValue: newAuthToken,
      })
    );
  }

  function logout() {
    window.localStorage.removeItem(BASIC_AUTH_STORAGE_KEY);
    // On localStoage.removeItem, the storage event is only triggered on other tabs and windows.
    // So we manually dispatch a storage event to trigger the subscribe function on the current window as well.
    window.dispatchEvent(
      new StorageEvent("storage", {
        key: BASIC_AUTH_STORAGE_KEY,
        newValue: null,
      })
    );
  }

  return {
    basicAuthToken,
    setBasciAuthToken,
    logout,
  };
}

export default useBasicAuthState;
