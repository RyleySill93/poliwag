import mem from 'mem/dist';
import axios from 'axios';

import authService from '../services/authService';

const refreshTokenFn = async () => {
  const session = authService.getSession();

  try {
    const result = await axios.post('/auth/refresh/', { refresh: session?.refresh });
    authService.handleAuthentication(result.data);
    return result;
  } catch (error) {
    authService.logout();
  }
};

const maxAge = 10000;

export const memoizedRefreshToken = mem(refreshTokenFn, {
  maxAge,
});
