import React from 'react';
import { SnackbarProvider } from 'notistack';
import { makeStyles } from '@mui/styles';

const useStyles = makeStyles((theme) => {
  const createStyle = (variant: string) => {
    // @ts-ignore
    const color = theme.palette[variant];
    return {
      color: `${color.contrastText} !important`,
      backgroundColor: `${color.main} !important`
    };
  };

  return {
    variantInfo: { ...createStyle('info') },
    variantSuccess: { ...createStyle('success') },
    variantWarning: { ...createStyle('warning') },
    variantError: { ...createStyle('error') }
  };
});

function NotistackProvider({ children }: { children: React.ReactNode }) {
  const classes = useStyles();

  return (
    <SnackbarProvider
      dense
      maxSnack={5}
      preventDuplicate
      hideIconVariant
      anchorOrigin={{
        vertical: 'top',
        horizontal: 'right'
      }}
      classes={classes}
    >
      {children}
    </SnackbarProvider>
  );
}

export default NotistackProvider;
