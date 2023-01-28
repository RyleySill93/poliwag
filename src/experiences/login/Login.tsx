import React from 'react';
import { useSnackbar } from 'notistack';

import TapClient from '../../utils/tapClient';
import authService from '../../services/authService';
import useUser from '../../hooks/useUser';
import Authenticate from './Authenticate';

const Login = () => {
  const { enqueueSnackbar } = useSnackbar();
  const [phone, setPhone] = React.useState('');
  const { refreshUser } = useUser();

  const confirmCode = (code: string) => new TapClient('/auth/phone/', ({ code, phone })).post().then((res) => {
    authService.handleAuthentication(res);
    // @ts-ignore
    refreshUser();
  }).catch((res) => {
    let message = 'Something went wrong.';
    if ([404, 400].includes(res.response.status) && res.response.data?.error) {
      message = res.response.data.error;
    }

    enqueueSnackbar(message, {
      variant: 'error'
    });
  });

  const onPhoneEntered = (_phone: string) => {
    new TapClient('/auth/phone/generate/', { phone: _phone }).post().then(() => setPhone(_phone)).catch((res) => {
      let message = 'Something went wrong.';
      if ([404, 400].includes(res.response.status) && res.response.data?.error) {
        message = res.response.data.error;
      }

      enqueueSnackbar(message, {
        variant: 'error'
      });
    });
  };

  return (
    <Authenticate
      title="Enter your phone number"
      subtitle="We'll send you a text so you can log into your account."
      onPhoneEntered={onPhoneEntered}
      confirmCode={confirmCode}
      phone={phone}
    />
  );
};

export default Login;
