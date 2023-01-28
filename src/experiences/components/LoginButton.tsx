import React from 'react';
import { Button, useTheme } from '@mui/material';
import { useNavigate } from 'react-router';

const LoginButton = () => {
  const theme = useTheme();
  const navigate = useNavigate();
  return (
    <Button
      size="small"
      variant="outlined"
      sx={{
        color: theme.palette.text.primary,
        border: `2px solid ${theme.palette.divider}`,
        borderRadius: '8px',
      }}
      onClick={() => navigate('/login')}
    >
      Login
    </Button>
  );
};

export default LoginButton;
