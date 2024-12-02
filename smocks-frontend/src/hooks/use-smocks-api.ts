import useBasicAuthState from "../auth/useAuthState";
import { snakeCaseToCamelCase } from "../utils";

enum SmockResponseStatus {
  SUCCESS = "success",
  FAIL = "fail",
  ERROR = "error",
}

type SmockResponse = {
  status: SmockResponseStatus;
  data: any; //object | object[];
};

enum OrderSide {
  BUY = "buy",
  SELL = "sell",
}

enum OrderType {
  MARKET = "market",
}

type Order = {
  assetId: string;
  type: OrderType;
  quantity: number;
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
    const defaultHeaders = _defaultHeaders();
    const headers = new Headers({
      ...Object.fromEntries(defaultHeaders.entries()),
      ...Object.fromEntries(new Headers(requestInit.headers).entries()),
    });
    requestInit.headers = headers;

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
      }
    );

    return getArtistResponse;
  }

  async function getMyAccount(): Promise<SmockResponse> {
    const getMyAccountResponse: SmockResponse = await _sendSmockApiRequest(
      `/accounts/me`,
      {
        method: "GET",
      }
    );

    return getMyAccountResponse;
  }

  async function getMyPositions(): Promise<SmockResponse> {
    const getMyPositionsResponse: SmockResponse = await _sendSmockApiRequest(
      `/positions/`,
      {
        method: "GET",
      }
    );

    if (getMyPositionsResponse.data) {
      getMyPositionsResponse.data = Object.values(getMyPositionsResponse.data);
    }

    return getMyPositionsResponse;
  }

  async function createPurchaseOrder({
    assetId,
    type,
    quantity,
  }: Order): Promise<SmockResponse> {
    return await _sendSmockApiRequest(`/orders/buy`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        asset_id: assetId,
        type,
        quantity,
      }),
    });
  }

  return {
    getArtist,
    getMyAccount,
    getMyPositions,
    createPurchaseOrder,
  };
}

export {
  OrderSide,
  OrderType,
  SmockResponseStatus,
  useNoAuthSmocksApi,
  useSmocksApi,
};
export type { Order };
