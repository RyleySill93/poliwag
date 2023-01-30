import React from 'react';
import { useRoutes } from 'react-router';

import useUser from './hooks/useUser';
import Login from './experiences/login/Login';

const Routes = () => {
  const { user } = useUser();

  const routes = [
    {
      path: '/login',
      element: <Login />,
      isHidden: Boolean(user),
    },
  ];

  const nonHiddenRoutes = routes.filter(({ isHidden }) => !isHidden);

  return useRoutes(nonHiddenRoutes);
};

export default Routes;
