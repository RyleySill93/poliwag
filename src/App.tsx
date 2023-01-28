import React from 'react';

import NotistackProvider from './providers/NotistackProvider';
import ThemePrimaryColor from './providers/ThemePrimaryColor';
import ThemeConfig from './theme';
import Routes from './Routes';
import useUser from './hooks/useUser';
import Loader from './components/Loader';

export default function App() {

  return <div>hi</div>
  debugger;
  const { userIsLoading } = useUser();

  return (
    <ThemeConfig>
      <ThemePrimaryColor>
        <NotistackProvider>
          {userIsLoading ? <Loader /> : <Routes />}
        </NotistackProvider>
      </ThemePrimaryColor>
    </ThemeConfig>
  );
}
