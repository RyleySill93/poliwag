import React from 'react';
import { Backdrop, Drawer as MuiDrawer } from '@mui/material';

interface Props {
    open: boolean;
    onClose: () => void;
    children: React.ReactNode;
}

const Drawer = ({ open, onClose, children }: Props) => (
  <>
    <Backdrop
      open={open}
      onClick={onClose}
      sx={{
        position: 'absolute',
        marginTop: '0px !important',
        paddingTop: 0,
        zIndex: 10,
      }}
    />
    <MuiDrawer
      open={open}
      onClose={onClose}
      anchor="bottom"
      PaperProps={{
        sx: {
          position: 'absolute',
          borderTopLeftRadius: '14px',
          borderTopRightRadius: '14px',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          width: '100%',
          maxHeight: '65%',
        }
      }}
      BackdropProps={{ style: { position: 'absolute' } }}
      ModalProps={{
        container: document.getElementById('layout'),
        style: { position: 'absolute' },
      }}
      variant="persistent"
    >
      {children}
    </MuiDrawer>
  </>
);

export default Drawer;
