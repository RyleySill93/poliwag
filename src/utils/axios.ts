// @ts-nocheck
import axios from 'axios';

import { memoizedRefreshToken } from './refreshToken';

axios.defaults.baseURL = process.env.REACT_APP_API_URL;

axios.interceptors.request.use(
  async (config) => {
    const rawSession = localStorage.getItem('session');

    const session = JSON.parse(rawSession);

    if (session?.accessToken) {
      config.headers = {
        ...config.headers,
        authorization: `Bearer ${session?.accessToken}`,
      };
    }

    return config;
  },
  (error) => Promise.reject(error)
);

axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const config = error?.config;

    if (error?.response?.status === 401 && !config?.sent) {
      config.sent = true;

      const result = await memoizedRefreshToken();

      if (result?.accessToken) {
        config.headers = {
          ...config.headers,
          authorization: `Bearer ${result?.accessToken}`,
        };
      }

      return axios(config);
    }
    return Promise.reject(error);
  }
);
