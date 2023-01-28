import React from 'react';
import { Box, Card, Typography } from '@mui/material';
import { SxProps } from '@mui/system';

interface Props {
    title: string;
    children: React.ReactNode;
    sx?: SxProps;
}

const InfoCard = ({ title, children, ...props }: Props) => (
  <Card {...props}>
    <Box p={2} width={150}>
      <Typography variant="subtitle2" color="textSecondary" pb={1}>
        {title}
      </Typography>
      {children}
    </Box>
  </Card>
);

export default InfoCard;
