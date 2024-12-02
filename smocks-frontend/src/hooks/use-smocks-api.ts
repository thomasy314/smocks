enum SmockResponseStatus {
  SUCCESS = "success",
  FAIL = "fail",
  ERROR = "error",
}

type SmockResponse = {
  status: SmockResponseStatus;
  data: object;
};

function useNoAuthSmocksApi() {
  async function login(username: string, password: string): Promise<boolean> {
    const loginResponse: SmockResponse = await fetch(`/api/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
      }),
    }).then(async (response) => response.json());

    return loginResponse.status === SmockResponseStatus.SUCCESS;
  }

  return {
    login,
  };
}

function useSmocksApi(basicAuthToken: string) {
  function _defaultHeaders() {
    const headers = new Headers();
    headers.set("Authorization", `Basic ${basicAuthToken}`);
    return headers;
  }

  async function getArtist(artist_id: string) {
    const getArtistResponse: SmockResponse = await fetch(
      `/api/artists/${artist_id}`,
      {
        method: "GET",
        headers: _defaultHeaders(),
      }
    ).then(async (response) => response.json());

    if (getArtistResponse.status === SmockResponseStatus.SUCCESS) {
      return getArtistResponse.data;
    }
  }

  async function getMyAccount() {
    const getArtistResponse: SmockResponse = await fetch(`/api/accounts/me`, {
      method: "GET",
      headers: _defaultHeaders(),
    }).then(async (response) => response.json());

    if (getArtistResponse.status === SmockResponseStatus.SUCCESS) {
      return getArtistResponse.data;
    }
  }

  return {
    getArtist,
    getMyAccount,
  };
}

export { useSmocksApi, useNoAuthSmocksApi as useSmocksNoAuthApi };
