// @ts-nocheck
import axios from 'axios';

import authService from '../services/authService';
import toCamelCase from './toCamelCase';
import toSnakeCase from './toSnakeCase';
import { memoizedRefreshToken } from './refreshToken';

const instance = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

axios.defaults.baseURL = process.env.REACT_APP_API_URL;

instance.interceptors.request.use(
  async (config) => {
    const session = authService.getSession();

    if (session?.access) {
      config.headers = {
        ...config.headers,
        authorization: `Bearer ${session?.access}`,
      };
    }

    return config;
  },
  (error) => Promise.reject(error)
);

instance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const config = error?.config;

    if (error?.response?.status === 401 && !config?.sent) {
      config.sent = true;

      const result = await memoizedRefreshToken();

      if (result?.access) {
        config.headers = {
          ...config.headers,
          authorization: `Bearer ${result?.access}`,
        };
      }

      return instance(config);
    }
    return Promise.reject(error);
  }
);

class TapClient {
  apiDomain: any;

  headers: any;

  payload: any;

  url: any;

  withAuth: any;

  withCasing: any;

  /*
  Little instance wrapper to talk to our backend.
  Makes it easy to send requests with/without authorization credentials
  and converts responses/payloads to/from camelCase and snakeCase
   */
  constructor(url: string, payload: any = null) {
    this.url = url;
    this.payload = payload || {};
    this.withAuth = true;
    this.withCasing = true;
    this.headers = {};
  }

  withoutCasing() {
    this.withCasing = false;
    return this;
  }

  _processResponse = (res: any) => (this.withCasing ? toCamelCase(res.data) : res.data);

  _processPayload(payload: any) {
    return this.withCasing ? toSnakeCase(payload) : payload;
  }

  get(stuff) {
    return instance.get(
      this.url,
      {
        ...stuff,
        params: this._processPayload(this.payload),
      },
    ).then(this._processResponse);
  }

  post() {
    return instance.post(
      this.url,
      this._processPayload(this.payload),
    ).then(this._processResponse);
  }

  patch() {
    return instance.patch(
      this.url,
      this._processPayload(this.payload),
    ).then(this._processResponse);
  }

  delete() {
    return instance.delete(
      this.url,
      {
        data: this._processPayload(this.payload),
      }
    ).then(this._processResponse);
  }
}

export default TapClient;
