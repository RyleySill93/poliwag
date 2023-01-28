import React from 'react';
import { Box, SxProps } from '@mui/material';
import { Icon } from '@iconify/react';
import checkmark from '@iconify/icons-eva/checkmark-fill';

interface Props {
    sx?: SxProps;
    checkColor?: string;
}

const CheckConfirmation = ({ sx, checkColor, ...props }: Props) => (
  <Box
    sx={{
      width: '140px',
      height: '140px',
      borderRadius: '100%',
      border: '1px solid #E7E8EC',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      backgroundColor: 'primary.light',
      filter: 'drop-shadow(0px 4px 4px rgba(0, 0, 0, 0.25))',
      ...sx,
    }}
    {...props}
  >
    <Icon icon={checkmark} width={50} height={50} color={checkColor || '#fff'} />
  </Box>
);

export default CheckConfirmation;
