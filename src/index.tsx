import 'react-perfect-scrollbar/dist/css/styles.css';
import React from 'react';

import { createRoot } from 'react-dom/client';
import { BrowserRouter } from 'react-router-dom';
import { HelmetProvider } from 'react-helmet-async';
import LocalizationProvider from '@mui/lab/LocalizationProvider';
import AdapterDateFns from '@mui/lab/AdapterDateFns';
import * as Sentry from '@sentry/react';

import { BrowserTracing } from '@sentry/tracing';
import { SettingsProvider } from './contexts/SettingsContext';

import App from './App';
import { UserProvider } from './contexts/UserContext';

// @ts-ignore
const root = createRoot(document.getElementById('root'));

if (process.env.REACT_APP_ENVIRONMENT === 'PRODUCTION') {
  Sentry.init({
    dsn: 'https://ba9c8f6d00a149eba798cadb1d8cc25b@o1293594.ingest.sentry.io/6662933',
    integrations: [new BrowserTracing()],

    // We recommend adjusting this value in production, or using tracesSampler
    // for finer control
    tracesSampleRate: 1.0,
  });
}

root.render(
  <HelmetProvider>
    <SettingsProvider>
      <UserProvider>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </UserProvider>
    </SettingsProvider>
  </HelmetProvider>
);

// @ts-ignore
if (module.hot) {
  // @ts-ignore
  module.hot.accept();
}
