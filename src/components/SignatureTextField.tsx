import React from 'react';
import { TextField } from '@mui/material';

const SignatureTextField = ({ ...props }) => (
  <TextField
    {...props}
    placeholder="Digital Signature"
    InputProps={{
      sx: {
        fontFamily: 'Ms Madi, Cursive',
        fontSize: 25,
      }
    }}
    fullWidth
    helperText={props.helperText}
  />
);

export default SignatureTextField;
