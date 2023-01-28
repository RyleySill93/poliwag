import React from 'react';
import { CircularProgress, Box } from '@mui/material';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles(() => ({
  wrapper: {
    width: '100%',
    height: '100%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
}));

const Loader = () => {
  const classes = useStyles();

  return (
    <Box className={classes.wrapper}>
      <CircularProgress />
    </Box>
  );
};

export default Loader;
