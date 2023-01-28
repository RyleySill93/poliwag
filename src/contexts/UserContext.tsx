import React, { ReactNode, createContext } from 'react';
import authService from '../services/authService';
import { UserType } from '../@types/user';

export type UserContextProps = {
    user?: UserType;
    portfolio?: any;
    userIsLoading?: boolean;
    refreshUser?: () => void;
};

const initialState: UserContextProps = {};

const UserContext = createContext(initialState);

type UserProviderProps = {
  children: ReactNode;
};

function UserProvider({ children }: UserProviderProps) {
  const isAuthenticated = authService.isAuthenticated();
  // const {
  //   result: user,
  //   isLoading: userIsLoading,
  //   httpRequest: refreshUser
  // } = useGetRequest({
  //   url: '/users/me/',
  //   shouldFetchOnInitialRender: isAuthenticated,
  // });
  const user = undefined;
  const refreshUser = () => {};

  return (
    <UserContext.Provider
      value={{
        user,
        refreshUser: refreshUser,
      }}
    >
      {children}
    </UserContext.Provider>
  );
}

export { UserProvider, UserContext };
