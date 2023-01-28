import React from 'react';
import { useNavigate } from 'react-router';
import json2mq from 'json2mq';

import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import Box from '@mui/material/Box';
import useMediaQuery from '@mui/material/useMediaQuery';

import { Divider } from '@mui/material';
import Logo from '../../components/Logo';
import LoginButton from './LoginButton';

type Props = {
    ContentProps?: any;
    withLogin?: boolean;
    footer?: React.ReactNode;
    children: React.ReactNode;
    noHeader?: boolean;
    rawLayout?: boolean; // For Persona and Sale Completed screens
};

const Layout = ({
  ContentProps,
  withLogin,
  footer,
  rawLayout,
  noHeader,
  children
}: Props) => {
  const navigate = useNavigate();
  const isMobile = useMediaQuery(
    json2mq({
      maxWidth: 600,
    }),
  );

  const content = (
    <Box
      id={isMobile ? 'content' : 'layout'}
      sx={{
        position: 'relative',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        minHeight: 'inherit',
      }}
    >
      {
        noHeader ? null : (
          <>
            <AppBar position="static" color="transparent" sx={{ boxShadow: 'none' }}>
              <Toolbar
                variant="dense"
                sx={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  pt: 1,
                }}
              >
                <Box onClick={() => navigate('/')}>
                  <Logo width={50} height={25} />
                </Box>
                {
            withLogin ? (
              <LoginButton />
            ) : (
              // <IconButton
              //   size="large"
              //   edge="start"
              //   color="inherit"
              //   aria-label="menu"
              // >
              //   <MenuIcon />
              // </IconButton>
              <Box />
            )
        }
              </Toolbar>
            </AppBar>
            <Divider />
          </>
        )
      }
      <Box
        px={3}
        pt={6}
        sx={{
          overflowY: 'auto',
          overflowX: 'hidden',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          flex: '1 1',
          minHeight: 'inherit',
        }}
        {...ContentProps}
      >
        {
              rawLayout ? children : (
                <>
                  <Box
                    display="flex"
                    flexGrow="1"
                    flexDirection="column"
                  >
                    {children}
                  </Box>
                  {
                      footer ? (
                        <Box py={3}>
                          {footer}
                        </Box>
                      ) : null
                    }
                </>
              )
          }
      </Box>
    </Box>
  );

  return isMobile ? content : (
    <Box
      display="flex"
      justifyContent="center"
      alignItems="center"
      height="100%"
    >
      <Box
        id="layout"
        sx={{
          width: 500,
          maxWidth: 500,
          minHeight: 700,
        }}
      >
        {content}
      </Box>
    </Box>
  );
};

export default Layout;
