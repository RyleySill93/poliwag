import React from 'react';
import Box from '@mui/material/Box';
import { useTheme } from '@mui/material';

const Footer = ({ children }: { children: React.ReactNode }) => {
  const theme = useTheme();
  return (
    <Box
      sx={{
        backgroundColor: theme.palette.background.default,
        top: 'auto',
        bottom: 0,
        position: 'absolute',
        width: '100%',
      }}
    >
      {children}
    </Box>
  );
};

export default Footer;
