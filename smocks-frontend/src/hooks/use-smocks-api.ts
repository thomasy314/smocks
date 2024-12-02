import useBasicAuthState from "../auth/useAuthState";
import { snakeCaseToCamelCase } from "../utils";

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
  const { logout: basicAuthLogout } = useBasicAuthState();

  async function login(
    username: string,
    password: string
  ): Promise<SmockResponse> {
    return fetch(`/api/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
      }),
    }).then(async (response) => response.json());
  }

  async function logout() {
    basicAuthLogout();
  }

  async function register(
    username: string,
    password: string
  ): Promise<SmockResponse> {
    return fetch(`/api/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        username,
        password,
      }),
    }).then(async (response) => response.json());
  }

  return {
    login,
    logout,
    register,
  };
}

function useSmocksApi(basicAuthToken: string) {
  function _defaultHeaders() {
    const headers = new Headers();
    headers.set("Authorization", `Basic ${basicAuthToken}`);
    return headers;
  }

  async function _sendSmockApiRequest(url: string, requestInit: RequestInit) {
    const request: SmockResponse = await fetch(`/api${url}`, requestInit).then(
      (response) => response.json()
    );

    if (request.status === SmockResponseStatus.SUCCESS) {
      request.data = snakeCaseToCamelCase(request.data);
    }

    return request;
  }

  async function getArtist(artist_id: string): Promise<SmockResponse> {
    const getArtistResponse: SmockResponse = await _sendSmockApiRequest(
      `/artists/${artist_id}`,
      {
        method: "GET",
        headers: _defaultHeaders(),
      }
    );

    return getArtistResponse;
  }

  async function getMyAccount(): Promise<SmockResponse> {
    const getArtistResponse: SmockResponse = await _sendSmockApiRequest(
      `/accounts/me`,
      {
        method: "GET",
        headers: _defaultHeaders(),
      }
    );

    return getArtistResponse;
  }

  return {
    getArtist,
    getMyAccount,
  };
}

export {
  SmockResponseStatus,
  useSmocksApi,
  useNoAuthSmocksApi as useSmocksNoAuthApi,
};
