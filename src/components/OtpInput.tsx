import React from 'react';
import { useTheme } from '@mui/styles';
import BaseOtpInput from './BaseOtpInput';

const OtpInput = ({ ...props }) => {
  const theme = useTheme();
  return (
    <BaseOtpInput
      {...props}
      numInputs={6}
      // @ts-ignore
      inputStyle={{
        width: '48px',
        height: '64px',
        fontSize: '30px',
        borderRadius: '8px',
        border: '1px solid rgba(0,0,0,0.3)',
        // @ts-ignore
        color: theme.palette.text.primary,
      }}
      // @ts-ignore
      focusStyle={{ outline: 'none', border: `2px solid ${theme.palette.primary.main}` }}
      containerStyle={{
        display: 'flex',
        justifyContent: 'space-between'
      }}
    />
  );
};

export default OtpInput;
